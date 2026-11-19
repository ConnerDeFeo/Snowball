import asyncio
import json
import logging
import threading
from typing import Awaitable, Callable, Optional
from edgar.sgml.sgml_parser import SECHTMLResponseError
from document_retrieval.FetchDocuments import FetchDocuments
from enums.FormType import FormType
from document_retrieval.ProxyData import build_proxy_data
from document_retrieval.financial_statements import build_statements
from document_retrieval.store_8k import store_8k
from document_retrieval.store_insider import store_insider
from utils.s3 import store
from utils.dynamo import documents_table

logger = logging.getLogger(__name__)

# Bounded to stay comfortably under SEC EDGAR's ~10 req/s fair-access guidance
# while still overlapping the many per-filing downloads for a wide date range.
MAX_FETCH_WORKERS = 8

# SEC sometimes returns a transient "File Unavailable" page instead of the filing.
FETCH_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 2


def _period_key(report) -> str:
    """Best-effort period string (YYYY-MM-DD) for a filing/report, falling
    back to filing_date when period_of_report is unavailable."""
    try:
        period = report.period_of_report
    except TypeError:
        # edgartools raises (instead of returning None) when the filing index
        # page has no dates, e.g. some DEF 14A proxies.
        period = None
    period = period or report.filing_date
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
    """Store one txt file per section, one sections.json with all of them, plus statements.json under `base`."""
    texts = {}
    for key, section in report.sections.items():
        text = section.text() or ""
        texts[key] = text
        store(f"{base}/{key}.txt", text.encode("utf-8"))
    store(f"{base}/sections.json", json.dumps(texts).encode("utf-8"))
    store(f"{base}/statements.json", json.dumps(build_statements(report)).encode("utf-8"))


def _store_10k(tckr: str, report, year: str):
    base = f"filings/{tckr}/{FormType.TEN_K.value}/{year}"
    _store_sectioned(report, base)


def _store_10q(tckr: str, report, year: str):
    period = _period_key(report)
    _, fp = _fiscal_focus(report)
    quarter = fp or f"Q{_quarter(period)}"
    base = f"filings/{tckr}/{FormType.TEN_Q.value}/{year}/{quarter}"
    _store_sectioned(report, base)


def _store_proxy(tckr: str, filing):
    # One folder per filing, so several proxies in the same year don't overwrite each other.
    base = f"filings/{tckr}/{FormType.PROXY.value}/{filing.filing_date}_{filing.accession_no}"
    store(f"{base}/proxy.txt", (filing.text() or "").encode("utf-8"))
    data = build_proxy_data(filing.obj())
    store(f"{base}/data.json", json.dumps(data).encode("utf-8"))


def _process_10k(tckr: str, filing):
    """Download (filing.obj()) then store a single 10-K. Runs in a worker thread."""
    thread_name = threading.current_thread().name
    logger.info("[%s] START  10-K  %s  filed %s", thread_name, tckr, filing.filing_date)
    _store_10k(tckr, filing.obj(), str(filing.filing_date)[:4])
    logger.info("[%s] DONE   10-K  %s  filed %s", thread_name, tckr, filing.filing_date)


def _process_10q(tckr: str, filing):
    """Download (filing.obj()) then store a single 10-Q. Runs in a worker thread."""
    thread_name = threading.current_thread().name
    logger.info("[%s] START  10-Q  %s  filed %s", thread_name, tckr, filing.filing_date)
    _store_10q(tckr, filing.obj(), str(filing.filing_date)[:4])
    logger.info("[%s] DONE   10-Q  %s  filed %s", thread_name, tckr, filing.filing_date)


def _process_proxy(tckr: str, filing):
    """Download (filing.text()) then store a single proxy. Runs in a worker thread."""
    thread_name = threading.current_thread().name
    logger.info("[%s] START  PROXY %s  filed %s", thread_name, tckr, filing.filing_date)
    _store_proxy(tckr, filing)
    logger.info("[%s] DONE   PROXY %s  filed %s", thread_name, tckr, filing.filing_date)


def _process_8k(tckr: str, filing):
    """Download then store a single 8-K as markdown. Runs in a worker thread."""
    thread_name = threading.current_thread().name
    logger.info("[%s] START  8-K   %s  filed %s", thread_name, tckr, filing.filing_date)
    store_8k(tckr, filing)
    logger.info("[%s] DONE   8-K   %s  filed %s", thread_name, tckr, filing.filing_date)


def _process_insider(tckr: str, filing):
    """Download then store a single Form 4 or 13D as markdown. Runs in a worker thread."""
    thread_name = threading.current_thread().name
    logger.info("[%s] START  %s  %s  filed %s", thread_name, filing.form, tckr, filing.filing_date)
    store_insider(tckr, filing)
    logger.info("[%s] DONE   %s  %s  filed %s", thread_name, filing.form, tckr, filing.filing_date)


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

    Layout (<year> is the year the filing was filed. 10-Q <quarter> is the fiscal
    period from XBRL DEI focus facts, falling back to the period's calendar quarter
    when XBRL is unavailable):
      filings/<tckr>/10-K/<year>/<section>.txt (+ sections.json, statements.json)
      filings/<tckr>/10-Q/<year>/Q<n>/<section>.txt (+ sections.json, statements.json)
      filings/<tckr>/DEF 14A/<filing_date>_<accession>/proxy.txt (+ data.json)
      filings/<tckr>/8-K/<filing_date>_<accession>/event.md (+ meta.json)
      filings/<tckr>/insiders/<filing_date>_<accession>/doc.md (+ meta.json)  (Form 4, 13D)

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
    eightk_filings = fetcher.fetch_multiple_8k(start_year, end_year)
    insider_filings = fetcher.fetch_multiple_insiders(start_year, end_year)

    counts = {
        FormType.TEN_K.value: len(tenk_filings),
        FormType.TEN_Q.value: len(tenq_filings),
        FormType.PROXY.value: len(proxy_filings),
        FormType.EIGHT_K.value: len(eightk_filings),
        "Insiders": len(insider_filings),
    }
    total = sum(counts.values())
    logger.info(
        "[pool] START  %s  spawning %d filing thread(s) (%d 10-K, %d 10-Q, %d proxy, %d 8-K)",
        tckr, total, counts[FormType.TEN_K.value], counts[FormType.TEN_Q.value],
        counts[FormType.PROXY.value], counts[FormType.EIGHT_K.value],
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
                # Complete task, retrying when SEC serves its transient "File Unavailable" page
                for attempt in range(1, FETCH_ATTEMPTS + 1):
                    try:
                        await asyncio.to_thread(fn, tckr, filing)
                        break
                    except SECHTMLResponseError:
                        if attempt == FETCH_ATTEMPTS:
                            raise
                        logger.warning(
                            "[retry] %s %s %s attempt %d failed, SEC returned HTML; retrying",
                            form, tckr, accession, attempt,
                        )
                        await asyncio.sleep(RETRY_DELAY_SECONDS * attempt)  # 2s, then 4s
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
    tasks += [_run(_process_8k, f, FormType.EIGHT_K.value) for f in eightk_filings]
    tasks += [_run(_process_insider, f, f.form) for f in insider_filings]

    await asyncio.gather(*tasks)  # re-raises first failure

    logger.info("[pool] DONE   %s  all %d filing thread(s) completed", tckr, total)

    return True
