import json

from enums.FormType import FormType
from utils.s3 import store


def _iso(d) -> str | None:
    return d.isoformat() if hasattr(d, "isoformat") else (str(d) if d else None)


# Primary 8-K document plus every exhibit (the press release is usually Ex. 99.1), as one markdown string.
def _event_markdown(filing) -> str:
    parts = []
    for att in filing.exhibits:  # first entry is the primary document
        if att.is_binary():
            continue
        body = att.markdown() or att.text()
        if body:
            parts.append(f"## {att.document_type} — {att.description}\n\n{body}")
    return "\n\n---\n\n".join(parts)


# Stores filings/{tckr}/8-K/{filing_date}_{accession}/event.md and meta.json.
def store_8k(tckr: str, filing):
    event_id = f"{_iso(filing.filing_date)}_{filing.accession_no}"
    base = f"filings/{tckr}/{FormType.EIGHT_K.value}/{event_id}"
    report = filing.obj()
    meta = {
        "id": event_id,
        "filing_date": _iso(filing.filing_date),
        "date_of_report": _iso(getattr(report, "date_of_report", None)),
        "items": list(getattr(report, "items", None) or []),
    }
    store(f"{base}/event.md", _event_markdown(filing).encode("utf-8"))
    store(f"{base}/meta.json", json.dumps(meta).encode("utf-8"))
