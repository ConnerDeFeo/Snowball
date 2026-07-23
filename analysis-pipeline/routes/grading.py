from fastapi import APIRouter

from grading.enums.RubricCategory import RubricCategory
from grading.grade_section import grade_section
from utils.sse import sse_response

router = APIRouter()


@router.get("/grade_section/{tckr}")
async def grade_section_route(
    tckr: str, start_year: int, end_year: int, rubric_category: RubricCategory
):
    async def job(on_progress):
        graded = await grade_section(tckr, start_year, end_year, rubric_category, on_progress=on_progress) # Hand down on_progress
        return {"type": "result", "graded": graded.model_dump(mode="json")}

    return sse_response(job) # Immeditley return the job
