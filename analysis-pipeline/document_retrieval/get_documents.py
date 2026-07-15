import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from document_retrieval.FetchDocuments import FetchDocuments
from document_retrieval.FormType import FormType
from utils.s3 import store

# Bounded to stay comfortably under SEC EDGAR's ~10 req/s fair-access guidance
# while still overlapping the many per-filing downloads for a wide date range.
MAX_FETCH_WORKERS = 8


def _period_key(report) -> str:
    """Best-effort period string (YYYY-MM-DD) for a filing/report, falling
    back to filing_date when period_of_report is unavailable."""
    return report.period_of_report or report.filing_date


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
    print(f"[{thread_name}] START  10-K  {tckr}  filed {filing.filing_date}")
    _store_10k(tckr, filing.obj())
    print(f"[{thread_name}] DONE   10-K  {tckr}  filed {filing.filing_date}")


def _process_10q(tckr: str, filing):
    """Download (filing.obj()) then store a single 10-Q. Runs in a worker thread."""
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] START  10-Q  {tckr}  filed {filing.filing_date}")
    _store_10q(tckr, filing.obj())
    print(f"[{thread_name}] DONE   10-Q  {tckr}  filed {filing.filing_date}")


def _process_proxy(tckr: str, filing):
    """Download (filing.text()) then store a single proxy. Runs in a worker thread."""
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] START  PROXY {tckr}  filed {filing.filing_date}")
    _store_proxy(tckr, filing)
    print(f"[{thread_name}] DONE   PROXY {tckr}  filed {filing.filing_date}")


def get_documents(tckr: str, from_date: str, to_date: str) -> bool:
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
    print(f"[pool] START  {tckr}  spawning {total} filing thread(s) "
          f"({len(tenk_filings)} 10-K, {len(tenq_filings)} 10-Q, {len(proxy_filings)} proxy)")

    with ThreadPoolExecutor(max_workers=MAX_FETCH_WORKERS) as executor:
        futures = []
        futures += [executor.submit(_process_10k, tckr, f) for f in tenk_filings]
        futures += [executor.submit(_process_10q, tckr, f) for f in tenq_filings]
        futures += [executor.submit(_process_proxy, tckr, f) for f in proxy_filings]

        for future in as_completed(futures):
            future.result()  # re-raise first failure

    print(f"[pool] DONE   {tckr}  all {total} filing thread(s) completed")

    return True
