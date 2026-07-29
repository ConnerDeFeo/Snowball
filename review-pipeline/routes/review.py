# routes/review.py
from uuid import uuid4

from fastapi import APIRouter
from context.get_manifest import *
from pydantic import BaseModel
from tools.agent import run_agent
from utils.dynamo import review_sessions_table
from utils.sse import sse_response

router = APIRouter()

class ReviewRequest(BaseModel):
    start_year: int
    end_year: int
    user_text: str
    session_id: str | None = None


@router.post("/review/{tckr}")
async def review(tckr:str, req: ReviewRequest):
    # 1. values come off the request body
    start_year, end_year, user_text = req.start_year, req.end_year, req.user_text
    session_id = req.session_id or str(uuid4())

    # 2. manifests for THIS company/window
    manifest_text = get_grade_manifest(tckr, start_year, end_year)
    findings_manifest_text = get_findings_manifest(tckr, start_year, end_year)
    history = review_sessions_table.get_history(session_id)

    async def job(on_progress):
        answer, updated_history = await run_agent(
            tckr, start_year, end_year, manifest_text, findings_manifest_text, user_text,
            history=history, on_progress=on_progress,
        )
        review_sessions_table.save_history(session_id, updated_history)
        return {"type": "result", "answer": answer, "session_id": session_id}

    return sse_response(job)
