import json

from document_retrieval.store_8k import _event_markdown, _iso
from utils.s3 import store

FOLDER = "insiders"


# "SC 13D/A" -> "13D", "SCHEDULE 13D" -> "13D", "4/A" -> "4"
def _short_form(form: str) -> str:
    return form.removesuffix("/A").removeprefix("SCHEDULE ").removeprefix("SC ")


def _num(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# One row per transaction on a Form 4.
def _transactions(summary) -> list[dict]:
    return [
        {
            "date": str(summary.reporting_date),
            "insider": summary.insider_name,
            "position": summary.position,
            "code": t.code,
            "description": t.description,
            "security_type": t.security_type,
            "shares": t.shares_numeric,
            "price": t.price_numeric,
            "value": t.value_numeric,
            "remaining": _num(summary.remaining_shares),
        }
        for t in getattr(summary, "transactions", [])
    ]


def _filer_and_transactions(form: str, report) -> tuple[str, list[dict]]:
    if form == "4":
        summary = report.get_ownership_summary()
        return summary.insider_name, _transactions(summary)
    persons = getattr(report, "reporting_persons", None) or []
    return (persons[0].name if persons else ""), []


# Stores filings/{tckr}/insiders/{filing_date}_{accession}/doc.md and meta.json.
def store_insider(tckr: str, filing):
    form = _short_form(filing.form)
    event_id = f"{_iso(filing.filing_date)}_{filing.accession_no}"
    base = f"filings/{tckr}/{FOLDER}/{event_id}"
    filer, transactions = _filer_and_transactions(form, filing.obj())
    meta = {
        "id": event_id,
        "form": form,
        "filing_date": _iso(filing.filing_date),
        "filer": filer,
        "transactions": transactions,
    }
    store(f"{base}/doc.md", (filing.markdown() or _event_markdown(filing)).encode("utf-8"))
    store(f"{base}/meta.json", json.dumps(meta).encode("utf-8"))
