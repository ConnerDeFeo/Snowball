from fastapi import APIRouter, HTTPException

from document_retrieval.store_insider import FOLDER
from events.read_events import list_metas, read_file

router = APIRouter()


# Metadata (incl. transactions) for every cached Form 4 / 13D in the year range (newest first).
@router.get("/insiders/{tckr}")
def list_insiders_route(tckr: str, start_year: int, end_year: int):
    return list_metas(tckr, FOLDER, start_year, end_year)


# Markdown body of one insider filing.
@router.get("/insiders/{tckr}/{filing_id}")
def get_insider_route(tckr: str, filing_id: str):
    markdown = read_file(tckr, FOLDER, filing_id, "doc.md")
    if markdown is None:
        raise HTTPException(status_code=404, detail="Filing not found")
    return {"markdown": markdown}
