# routes/health.py
from fastapi import APIRouter
from pydantic import BaseModel

from grading.enums.RubricCategory import RubricCategory
from grading.grade_section import grade_section

router = APIRouter()

class GradeRequest(BaseModel):
    start_year: int
    end_year: int

@router.post("/grade_company/{tckr}")
def grade(tckr: str, grade_request: GradeRequest):
    return {"status": "ok"}

class GradeSectionRequest(BaseModel):
    start_date: str
    end_date: str
    rubric_category: RubricCategory

@router.post("/grade_section/{tckr}")
def grade_section_route(tckr: str, grade_section_request: GradeSectionRequest):
    return grade_section(
        tckr,
        grade_section_request.start_date,
        grade_section_request.end_date,
        grade_section_request.rubric_category,
    )
