# routes/health.py
from fastapi import APIRouter
from context.get_manifest import *
from pydantic import BaseModel
from tools.agent import run_agent

router = APIRouter()

class ReviewRequest(BaseModel):
    start_date: str
    end_date: str
    user_text: str
    

@router.post("/review/{tckr}")
def review(tckr:str, req: ReviewRequest):
    # 1. values come off the request body
    start_date, end_date, user_text = req.start_date, req.end_date, req.user_text

    # 2. manifest for THIS company/window
    manifest_text = get_manifest(tckr, start_date, end_date)

    return run_agent(tckr, start_date, end_date, manifest_text, user_text)