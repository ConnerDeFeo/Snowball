import json
from concurrent.futures import ThreadPoolExecutor

from botocore.exceptions import ClientError

from enums.FormType import FormType
from utils.s3 import list_keys, retrieve

META = "meta.json"


# Metadata for every filing under filings/{tckr}/{folder}/ filed in the year range, newest first.
# Keys are .../{folder}/{filing_date}_{accession}/meta.json, so the year is the first 4 chars of the id.
def list_metas(tckr: str, folder: str, start_year: int, end_year: int) -> list[dict]:
    prefix = f"filings/{tckr}/{folder}/"
    keys = [
        k for k in list_keys(prefix)
        if k.endswith(f"/{META}") and start_year <= int(k[len(prefix):][:4]) <= end_year
    ]
    with ThreadPoolExecutor(max_workers=16) as pool:
        metas = list(pool.map(lambda k: json.loads(retrieve(k)), keys))
    metas.sort(key=lambda m: m["id"], reverse=True)
    return metas


# Text of one cached file, or None if it isn't cached.
def read_file(tckr: str, folder: str, item_id: str, name: str) -> str | None:
    try:
        return retrieve(f"filings/{tckr}/{folder}/{item_id}/{name}").decode("utf-8")
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise


def list_events(tckr: str, start_year: int, end_year: int) -> list[dict]:
    return list_metas(tckr, FormType.EIGHT_K.value, start_year, end_year)


def read_event(tckr: str, event_id: str) -> str | None:
    return read_file(tckr, FormType.EIGHT_K.value, event_id, "event.md")
