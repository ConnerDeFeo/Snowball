# routes/review.py
import asyncio
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter
from context.checklist_manifest import get_checklist_manifest
from context.mentions import render_mentions
from filings.manifest import filings_manifest
from pydantic import BaseModel
from tools.agent import run_agent
from utils.dynamo import review_sessions_table
from utils.sse import sse_response

router = APIRouter()

# A filing section the user @-mentioned. quarter is None for a 10-K.
class Mention(BaseModel):
    form: str
    year: str
    quarter: str | None = None
    section: str

class ReviewRequest(BaseModel):
    start_year: int
    end_year: int
    user_text: str
    session_id: str | None = None
    mentions: list[Mention] = []
    model: Literal["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"] = "claude-haiku-5-5"


@router.post("/review/{tckr}")
async def review(tckr:str, req: ReviewRequest):
    # 1. values come off the request body
    start_year, end_year, user_text = req.start_year, req.end_year, req.user_text
    session_id = req.session_id or str(uuid4())

    # 2. context for THIS company/window (blocking S3/HTTP/Dynamo calls, so off the event loop)
    mentions_text, filings_text, checklist_text, history = await asyncio.gather(
        asyncio.to_thread(render_mentions, tckr, [m.model_dump() for m in req.mentions]),
        asyncio.to_thread(filings_manifest, tckr, start_year, end_year),
        asyncio.to_thread(get_checklist_manifest),
        asyncio.to_thread(review_sessions_table.get_history, session_id),
    )

    async def job(on_progress):
        answer, updated_history = await run_agent(
            tckr, start_year, end_year, mentions_text, filings_text, checklist_text, user_text,
            history=history, on_progress=on_progress, model=req.model,
        )
        review_sessions_table.save_history(session_id, updated_history)
        return {"type": "result", "answer": answer, "session_id": session_id}

    return sse_response(job)
