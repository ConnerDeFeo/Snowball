import asyncio
import json
import logging
import threading
from typing import Awaitable, Callable, Optional
from document_retrieval.FetchDocuments import FetchDocuments
from document_retrieval.FormType import FormType
from document_retrieval.ProxyData import build_proxy_data
from utils.s3 import store
from utils.dynamo import documents_table

logger = logging.getLogger(__name__)

# Bounded to stay comfortably under SEC EDGAR's ~10 req/s fair-access guidance
# while still overlapping the many per-filing downloads for a wide date range.
MAX_FETCH_WORKERS = 8


def _period_key(report) -> str:
    """Best-effort period string (YYYY-MM-DD) for a filing/report, falling
    back to filing_date when period_of_report is unavailable."""
    period = report.period_of_report or report.filing_date
    if hasattr(period, "isoformat"):
        return period.isoformat()
    return str(period)


def _year(period: str) -> str:
    return period[:4]


def _quarter(period: str) -> int:
    month = int(period[5:7])
    return (month - 1) // 3 + 1


def _fiscal_focus(report):
    """(fiscal_year, fiscal_period) from XBRL DEI focus facts, or (None, None)
    if the filing has no XBRL data. fiscal_period is "FY", "Q1".."Q4"."""
    fin = getattr(report, "financials", None)
    xb = getattr(fin, "xb", None) if fin is not None else None
    if xb is None:
        return None, None
    info = xb.entity_info
    fy = info.get("fiscal_year")
    fp = info.get("fiscal_period")
    return (str(fy) if fy else None), (fp or None)


def _store_sectioned(report, base: str):
    """Store one txt file per section plus a combined sections.json under `base`."""
    sections = {}
    for key, section in report.sections.items():
        text = section.text() or ""
        store(f"{base}/{key}.txt", text.encode("utf-8"))
        sections[key] = text
    store(f"{base}/sections.json", json.dumps(sections).encode("utf-8"))


def _store_10k(tckr: str, report):
    fy, _ = _fiscal_focus(report)
    year = fy or _year(_period_key(report))
    base = f"filings/{tckr}/{FormType.TEN_K.value}/{year}"
    _store_sectioned(report, base)


def _store_10q(tckr: str, report):
    period = _period_key(report)
    fy, fp = _fiscal_focus(report)
    year = fy or _year(period)
    quarter = fp or f"Q{_quarter(period)}"
    base = f"filings/{tckr}/{FormType.TEN_Q.value}/{year}/{quarter}"
    _store_sectioned(report, base)


def _store_proxy(tckr: str, filing):
    year = _year(_period_key(filing))
    base = f"filings/{tckr}/{FormType.PROXY.value}/{year}"
    store(f"{base}/proxy.txt", (filing.text() or "").encode("utf-8"))
    data = build_proxy_data(filing.obj())
    store(f"{base}/data.json", json.dumps(data).encode("utf-8"))


def _process_10k(tckr: str, filing):
    """Download (filing.obj()) then store a single 10-K. Runs in a worker thread."""
    thread_name = threading.current_thread().name
    logger.info("[%s] START  10-K  %s  filed %s", thread_name, tckr, filing.filing_date)
    _store_10k(tckr, filing.obj())
    logger.info("[%s] DONE   10-K  %s  filed %s", thread_name, tckr, filing.filing_date)


def _process_10q(tckr: str, filing):
    """Download (filing.obj()) then store a single 10-Q. Runs in a worker thread."""
    thread_name = threading.current_thread().name
    logger.info("[%s] START  10-Q  %s  filed %s", thread_name, tckr, filing.filing_date)
    _store_10q(tckr, filing.obj())
    logger.info("[%s] DONE   10-Q  %s  filed %s", thread_name, tckr, filing.filing_date)


def _process_proxy(tckr: str, filing):
    """Download (filing.text()) then store a single proxy. Runs in a worker thread."""
    thread_name = threading.current_thread().name
    logger.info("[%s] START  PROXY %s  filed %s", thread_name, tckr, filing.filing_date)
    _store_proxy(tckr, filing)
    logger.info("[%s] DONE   PROXY %s  filed %s", thread_name, tckr, filing.filing_date)


async def get_documents(
    tckr: str,
    start_year: int,
    end_year: int,
    # Callabe function that takes dict param and returns awaitable nothing
    on_progress: Optional[Callable[[dict], Awaitable[None]]] = None,
) -> bool:
    """
    Fetch every 10-K, 10-Q, and DEF 14A proxy statement for `tckr` filed within
    [start_year, end_year] and cache them to S3.

    Layout (10-K/10-Q <year>/quarter are fiscal, from XBRL DEI focus facts,
    falling back to calendar-derived values when XBRL is unavailable; DEF 14A
    stays calendar-derived since proxies have no XBRL fiscal data):
      filings/<tckr>/10-K/<year>/<section>.txt (+ sections.json)
      filings/<tckr>/10-Q/<year>/Q<n>/<section>.txt (+ sections.json)
      filings/<tckr>/DEF 14A/<year>/proxy.txt

    If `on_progress` is given, it's awaited with a "start" event before any
    downloads begin and a "progress" event after each filing completes —
    lets a caller (e.g. an SSE route) stream progress to a client.

    Returns False if `tckr` could not be resolved to a company, True otherwise.
    """
    fetcher = FetchDocuments.create(tckr)
    if fetcher is None:
        return False

    # These list/filter calls are lightweight index lookups, not downloads —
    # the actual filing content is fetched lazily inside the worker threads
    # below, so all the slow network I/O runs in parallel.
    tenk_filings = fetcher.fetch_multiple_10k(start_year, end_year)
    tenq_filings = fetcher.fetch_multiple_10q(start_year, end_year)
    proxy_filings = fetcher.fetch_multiple_proxy(start_year, end_year)

    counts = {
        FormType.TEN_K.value: len(tenk_filings),
        FormType.TEN_Q.value: len(tenq_filings),
        FormType.PROXY.value: len(proxy_filings),
    }
    total = sum(counts.values())
    logger.info(
        "[pool] START  %s  spawning %d filing thread(s) (%d 10-K, %d 10-Q, %d proxy)",
        tckr, total, counts[FormType.TEN_K.value], counts[FormType.TEN_Q.value], counts[FormType.PROXY.value],
    )

    # Function handed down for progress updates 
    if on_progress:
        await on_progress({"type": "start", "total": total, "counts": counts})

    # Cap concurrent worker threads to MAX_FETCH_WORKERS
    sem = asyncio.Semaphore(MAX_FETCH_WORKERS)
    completed = 0

    async def _run(fn, filing, form: str):
        nonlocal completed
        accession = filing.accession_no
        # Check complepted status
        existing = await asyncio.to_thread(documents_table.get, accession)
        if not existing or existing.get("status") != "processed":
            await asyncio.to_thread(documents_table.put, accession, status="processing")
            # Await semephore lock
            async with sem:
                # Complete task
                await asyncio.to_thread(fn, tckr, filing)
            await asyncio.to_thread(documents_table.put, accession, status="processed")
        # If update progress function given, update client
        if on_progress:
            completed += 1
            await on_progress({
                "type": "progress",
                "completed": completed,
                "total": total,
                "form": form,
                "filing_date": str(filing.filing_date),
            })

    tasks = []
    tasks += [_run(_process_10k, f, FormType.TEN_K.value) for f in tenk_filings]
    tasks += [_run(_process_10q, f, FormType.TEN_Q.value) for f in tenq_filings]
    tasks += [_run(_process_proxy, f, FormType.PROXY.value) for f in proxy_filings]

    await asyncio.gather(*tasks)  # re-raises first failure

    logger.info("[pool] DONE   %s  all %d filing thread(s) completed", tckr, total)

    return True
