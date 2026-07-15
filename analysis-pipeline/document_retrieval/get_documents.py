import asyncio
import json
import logging
import threading
from document_retrieval.FetchDocuments import FetchDocuments
from document_retrieval.FormType import FormType
from utils.s3 import store

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


def _store_sectioned(report, base: str):
    """Store one txt file per section plus a combined sections.json under `base`."""
    sections = {}
    for key, section in report.sections.items():
        text = section.text() or ""
        store(f"{base}/{key}.txt", text.encode("utf-8"))
        sections[key] = text
    store(f"{base}/sections.json", json.dumps(sections).encode("utf-8"))


def _store_10k(tckr: str, report):
    year = _year(_period_key(report))
    base = f"filings/{tckr}/{FormType.TEN_K.value}/{year}"
    _store_sectioned(report, base)


def _store_10q(tckr: str, report):
    period = _period_key(report)
    year, quarter = _year(period), _quarter(period)
    base = f"filings/{tckr}/{FormType.TEN_Q.value}/{year}/Q{quarter}"
    _store_sectioned(report, base)


def _store_proxy(tckr: str, filing):
    year = _year(_period_key(filing))
    key = f"filings/{tckr}/{FormType.PROXY.value}/{year}/proxy.txt"
    store(key, (filing.text() or "").encode("utf-8"))


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


async def get_documents(tckr: str, from_date: str, to_date: str) -> bool:
    """
    Fetch every 10-K, 10-Q, and DEF 14A proxy statement for `tckr` filed within
    [from_date, to_date] and cache them to S3.

    Layout:
      filings/<tckr>/10-K/<year>/<section>.txt (+ sections.json)
      filings/<tckr>/10-Q/<year>/Q<n>/<section>.txt (+ sections.json)
      filings/<tckr>/DEF 14A/<year>/proxy.txt

    Returns False if `tckr` could not be resolved to a company, True otherwise.
    """
    fetcher = FetchDocuments.create(tckr)
    if fetcher is None:
        return False

    # These list/filter calls are lightweight index lookups, not downloads —
    # the actual filing content is fetched lazily inside the worker threads
    # below, so all the slow network I/O runs in parallel.
    tenk_filings = fetcher.fetch_multiple_10k(from_date, to_date)
    tenq_filings = fetcher.fetch_multiple_10q(from_date, to_date)
    proxy_filings = fetcher.fetch_multiple_proxy(from_date, to_date)

    total = len(tenk_filings) + len(tenq_filings) + len(proxy_filings)
    logger.info(
        "[pool] START  %s  spawning %d filing thread(s) (%d 10-K, %d 10-Q, %d proxy)",
        tckr, total, len(tenk_filings), len(tenq_filings), len(proxy_filings),
    )

    # Cap concurrent worker threads at MAX_FETCH_WORKERS (same bound the old
    # ThreadPoolExecutor enforced) since asyncio.to_thread() alone would run
    # against the default executor's much larger thread limit.
    sem = asyncio.Semaphore(MAX_FETCH_WORKERS)

    async def _run(fn, filing):
        async with sem:
            await asyncio.to_thread(fn, tckr, filing)

    tasks = []
    tasks += [_run(_process_10k, f) for f in tenk_filings]
    tasks += [_run(_process_10q, f) for f in tenq_filings]
    tasks += [_run(_process_proxy, f) for f in proxy_filings]

    await asyncio.gather(*tasks)  # re-raises first failure

    logger.info("[pool] DONE   %s  all %d filing thread(s) completed", tckr, total)

    return True
