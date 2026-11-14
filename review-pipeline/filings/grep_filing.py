import json
import re

from botocore.exceptions import ClientError

from utils.s3 import retrieve

MAX_HITS = 20
CONTEXT_CHARS = 200

# Key layout matches filings/read_section.py: filings/{tckr}/{form}/{year}[/{quarter}]/sections.json
# Returns None if that filing's sections.json isn't cached.
def grep_filing(tckr: str, form: str, year: str, quarter: str | None, pattern: str) -> str | None:
    try:
        rx = re.compile(pattern, re.IGNORECASE)
    except re.error as e:
        return f"invalid regex: {e}"

    middle = f"{year}/{quarter}" if quarter else year
    try:
        sections = json.loads(retrieve(f"filings/{tckr}/{form}/{middle}/sections.json"))
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise

    hits = []
    total = 0
    for name, text in sections.items():
        for m in rx.finditer(text):
            total += 1
            if len(hits) < MAX_HITS:
                snippet = text[max(0, m.start() - CONTEXT_CHARS):m.end() + CONTEXT_CHARS]
                hits.append(f"[{name}] …{snippet}…")

    if not hits:
        return "no matches"
    if total > MAX_HITS:
        hits.append(f"({total - MAX_HITS} more matches, narrow your pattern)")
    return "\n---\n".join(hits)
