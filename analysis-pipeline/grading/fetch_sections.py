from document_retrieval.FormType import FormType
from enums.TenKSections import TenKSection
from enums.TenQSections import TenQSection
from utils.s3 import list_keys, retrieve


def _in_range(year: int, start_year: int, end_year: int) -> bool:
    return start_year <= year <= end_year


def _fetch_10k_sections(tckr: str, sections: set[str], start_year: int, end_year: int) -> list[dict]:
    # 10-K keys: filings/{tckr}/{form}/{year}/{section}.txt
    prefix = f"filings/{tckr}/{FormType.TEN_K.value}/"
    blocks = []
    for key in list_keys(prefix):
        year_str, filename = key[len(prefix):].split("/")
        section = filename.removesuffix(".txt")
        if section not in sections or not _in_range(int(year_str), start_year, end_year):
            continue  # not a requested section, or filing year outside the window
        blocks.append({
            "form": FormType.TEN_K.value, "year": year_str, "section": section,
            "text": retrieve(key).decode("utf-8"),  # actual S3 fetch happens here
        })
    return blocks


def _fetch_10q_sections(tckr: str, sections: set[str], start_year: int, end_year: int) -> list[dict]:
    # 10-Q keys: filings/{tckr}/{form}/{year}/{quarter}/{section}.txt
    prefix = f"filings/{tckr}/{FormType.TEN_Q.value}/"
    blocks = []
    for key in list_keys(prefix):
        year_str, quarter, filename = key[len(prefix):].split("/")
        section = filename.removesuffix(".txt")
        if section not in sections or not _in_range(int(year_str), start_year, end_year):
            continue
        blocks.append({
            "form": FormType.TEN_Q.value, "year": year_str, "quarter": quarter, "section": section,
            "text": retrieve(key).decode("utf-8"),
        })
    return blocks


def fetch_sections(tckr: str, start_date: str, end_date: str, locations: list[TenKSection | TenQSection]) -> list[dict]:
    """Fetch the cached S3 section text for each TenKSection/TenQSection in
    `locations`, restricted to filings whose year falls within
    [start_date, end_date]. Missing sections/filings are skipped silently."""
    # split requested locations by form type, since each is stored under a different key layout
    tenk_sections = {loc.value for loc in locations if isinstance(loc, TenKSection)}
    tenq_sections = {loc.value for loc in locations if isinstance(loc, TenQSection)}
    start_year, end_year = int(start_date[:4]), int(end_date[:4])

    blocks = []
    if tenk_sections:
        blocks += _fetch_10k_sections(tckr, tenk_sections, start_year, end_year)
    if tenq_sections:
        blocks += _fetch_10q_sections(tckr, tenq_sections, start_year, end_year)
    return blocks
