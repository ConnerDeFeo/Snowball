from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from document_retrieval.get_documents import get_documents

router = APIRouter()

MAX_YEARS = 6


class DocumentsRequest(BaseModel):
    from_date: Optional[str] = None
    to_date: Optional[str] = None


@router.post("/documents/{tckr}")
async def documents(tckr: str, body: DocumentsRequest):
    from_date = body.from_date
    to_date = body.to_date
    if not from_date or not to_date:
        raise HTTPException(status_code=400, detail="from_date and to_date are required")

    from_year, to_year = int(from_date[:4]), int(to_date[:4])
    if to_year < from_year or to_year - from_year >= MAX_YEARS:
        raise HTTPException(status_code=400, detail=f"date range may span at most {MAX_YEARS} years")

    found = await get_documents(tckr, from_date, to_date)
    if not found:
        raise HTTPException(status_code=404, detail=f"no company found for ticker: {tckr}")

    return {"status": "ok", "ticker": tckr}
