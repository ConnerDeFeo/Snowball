# routes/health.py
from fastapi import APIRouter
from context.get_manifest import *
from pydantic import BaseModel
from tools.agent import run_agent

router = APIRouter()

class ReviewRequest(BaseModel):
    start: str
    end: str
    

@router.post("/review/{tckr}")
def review(tckr:str, req: ReviewRequest):
    # 1. values come off the request body
    start, end = req.start, req.end

    # 2. manifest for THIS company/window
    manifest_text = get_manifest(tckr, start, end)

    return run_agent(tckr, start, end, manifest_text)