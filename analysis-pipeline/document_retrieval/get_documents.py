import json
from concurrent.futures import ThreadPoolExecutor
from document_retrieval.FetchDocuments import FetchDocuments
from document_retrieval.FormType import FormType
from utils.s3 import store


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

    tenks = fetcher.fetch_multiple_10k(from_date, to_date)
    tenqs = fetcher.fetch_multiple_10q(from_date, to_date)
    proxies = fetcher.fetch_multiple_proxy(from_date, to_date)

    with ThreadPoolExecutor() as executor:
        futures = []
        futures += [executor.submit(_store_10k, tckr, report) for report in tenks]
        futures += [executor.submit(_store_10q, tckr, report) for report in tenqs]
        futures += [executor.submit(_store_proxy, tckr, filing) for filing in proxies]

        for future in futures:
            future.result()

    return True
