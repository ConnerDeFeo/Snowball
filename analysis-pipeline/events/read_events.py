import json
from concurrent.futures import ThreadPoolExecutor

from botocore.exceptions import ClientError

from enums.FormType import FormType
from utils.s3 import list_keys, retrieve

META = "meta.json"


def _prefix(tckr: str) -> str:
    return f"filings/{tckr}/{FormType.EIGHT_K.value}/"


# Metadata (id, filing_date, date_of_report, items) for every 8-K filed in the year range, newest first.
# Keys are filings/{tckr}/8-K/{filing_date}_{accession}/meta.json, so the year is the first 4 chars of the folder.
def list_events(tckr: str, start_year: int, end_year: int) -> list[dict]:
    prefix = _prefix(tckr)
    keys = [
        k for k in list_keys(prefix)
        if k.endswith(f"/{META}") and start_year <= int(k[len(prefix):][:4]) <= end_year
    ]
    with ThreadPoolExecutor(max_workers=16) as pool:
        events = list(pool.map(lambda k: json.loads(retrieve(k)), keys))
    events.sort(key=lambda e: e["id"], reverse=True)
    return events


# Markdown body of one 8-K, or None if it isn't cached.
def read_event(tckr: str, event_id: str) -> str | None:
    try:
        return retrieve(f"{_prefix(tckr)}{event_id}/event.md").decode("utf-8")
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise
