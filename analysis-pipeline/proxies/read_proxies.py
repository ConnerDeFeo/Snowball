import json

from enums.FormType import FormType
from utils.s3 import list_keys, retrieve

FILE_NAME = "data.json"


# Reads the cached DEF 14A data for every proxy filed in the year range (newest first).
# Keys are filings/{tckr}/DEF 14A/{filing_date}_{accession}/data.json.
def read_proxies(tckr: str, start_year: int, end_year: int) -> list[dict]:
    prefix = f"filings/{tckr}/{FormType.PROXY.value}/"
    proxies = []
    for key in list_keys(prefix):
        parts = key[len(prefix):].split("/")
        if len(parts) != 2 or parts[1] != FILE_NAME or not start_year <= int(parts[0][:4]) <= end_year:
            continue
        proxies.append({"id": parts[0], "filing_date": parts[0][:10], "data": json.loads(retrieve(key))})
    proxies.sort(key=lambda p: p["id"], reverse=True)
    return proxies
