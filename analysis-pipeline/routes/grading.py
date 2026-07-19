# routes/health.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class GradeRequest(BaseModel):
    start_year: int
    end_year: int

@router.post("/grade_company/{tckr}")
def grade(tckr: str, grade_request: GradeRequest):
    return {"status": "ok"}
