import json

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
    filings.sort(key=lambda f: sort_key(f["year"], f["quarter"]), reverse=True)
    return filings
