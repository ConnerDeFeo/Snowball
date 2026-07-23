from fastapi import APIRouter, HTTPException

from document_retrieval.get_documents import get_documents
from utils.sse import sse_response

router = APIRouter()

MAX_YEARS = 6


@router.get("/documents/{tckr}")
async def documents(tckr: str, start_year: int, end_year: int):
    # Range validation
    if end_year < start_year or end_year - start_year >= MAX_YEARS:
        raise HTTPException(status_code=400, detail=f"date range may span at most {MAX_YEARS} years")

    async def job(on_progress):
        found = await get_documents(tckr, start_year, end_year, on_progress=on_progress)
        if not found:
            return {"type": "error", "detail": f"no company found for ticker: {tckr}"}
        return {"type": "done", "ticker": tckr}

    return sse_response(job)
