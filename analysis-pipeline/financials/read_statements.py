import json

from document_retrieval.financial_statements import PERIOD_COLUMN
from enums.FormType import FormType
from evidence.plan_work import sort_key
from utils.s3 import list_keys, retrieve

FILE_NAME = "statements.json"


# Splits a statements key into (year, quarter), or None for any other file.
# 10-K keys are filings/{tckr}/10-K/{year}/statements.json, 10-Q keys have a
# quarter folder before the file.
def _parse(key: str, prefix: str) -> tuple[str, str | None] | None:
    parts = key[len(prefix):].split("/")
    if parts[-1] != FILE_NAME:
        return None
    return parts[0], parts[1] if len(parts) == 3 else None


# Latest period end date (YYYY-MM-DD) among a filing's statement columns, which are named
# by end date. Orders filings by when they were filed, since a later filing ends later.
def _period_end(statements: dict) -> str:
    return max(
        (str(c)[:10] for s in statements.values() for c in s["columns"] if PERIOD_COLUMN.match(str(c))),
        default="",
    )


def read_statements(tckr: str, start_year: int, end_year: int) -> list[dict]:
    filings = []
    for form in (FormType.TEN_K.value, FormType.TEN_Q.value):
        prefix = f"filings/{tckr}/{form}/"
        for key in list_keys(prefix):
            parsed = _parse(key, prefix)
            if parsed is None or not start_year <= int(parsed[0]) <= end_year:
                continue
            year, quarter = parsed
            filings.append({
                "form": form, "year": year, "quarter": quarter,
                "statements": json.loads(retrieve(key)),
            })
    # Newest first by period end (a 10-K can fall before or after that year's 10-Qs);
    # filings without statements fall back to year/quarter order.
    filings.sort(key=lambda f: (_period_end(f["statements"]), sort_key(f["year"], f["quarter"])), reverse=True)
    return filings
