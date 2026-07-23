# routes/health.py
from fastapi import APIRouter
from context.get_manifest import *
from pydantic import BaseModel
from tools.agent import run_agent

router = APIRouter()

class ReviewRequest(BaseModel):
    start_year: int
    end_year: int
    user_text: str


@router.post("/review/{tckr}")
def review(tckr:str, req: ReviewRequest):
    # 1. values come off the request body
    start_year, end_year, user_text = req.start_year, req.end_year, req.user_text

    # 2. manifests for THIS company/window
    manifest_text = get_grade_manifest(tckr, start_year, end_year)
    findings_manifest_text = get_findings_manifest(tckr, start_year, end_year)

    return run_agent(tckr, start_year, end_year, manifest_text, findings_manifest_text, user_text)