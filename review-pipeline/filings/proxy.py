import re

from botocore.exceptions import ClientError

from filings.grep_filing import CONTEXT_CHARS, MAX_HITS
from utils.s3 import retrieve

READ_CHARS = 8000
LEAD_IN_CHARS = 1000


# Key layout: filings/{tckr}/DEF 14A/{filing_date}_{accession}/proxy.txt
# Returns None if that proxy isn't cached.
def _load(tckr: str, proxy_id: str) -> str | None:
    try:
        return retrieve(f"filings/{tckr}/DEF 14A/{proxy_id}/proxy.txt").decode("utf-8")
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise


# A proxy has no sections, so each hit is labeled with its character offset (for read_proxy).
def grep_proxy(tckr: str, proxy_id: str, pattern: str) -> str | None:
    try:
        rx = re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        return f"invalid regex: {e}"

    text = _load(tckr, proxy_id)
    if text is None:
        return None

    hits = []
    total = 0
    for m in rx.finditer(text):
        total += 1
        if len(hits) < MAX_HITS:
            snippet = text[max(0, m.start() - CONTEXT_CHARS):m.end() + CONTEXT_CHARS]
            hits.append(f"[offset {m.start()}] …{snippet}…")

    if not hits:
        return "no matches"
    if total > MAX_HITS:
        hits.append(f"({total - MAX_HITS} more matches, narrow your pattern)")
    return "\n---\n".join(hits)


# One passage of the proxy, starting a little before `offset` so a grep hit has lead-in.
def read_proxy(tckr: str, proxy_id: str, offset: int) -> str | None:
    text = _load(tckr, proxy_id)
    if text is None:
        return None
    start = max(0, offset - LEAD_IN_CHARS)
    end = min(len(text), start + READ_CHARS)
    return f"{text[start:end]}\n(chars {start}-{end} of {len(text)})"
