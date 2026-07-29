from fastapi import APIRouter

from grading.grade_query import get_latest_grades
from grading.types.GradedTimePeriod import GradedTimePeriod

router = APIRouter()


@router.get("/grades/{tckr}", response_model=list[GradedTimePeriod])
def get_grades(tckr: str, start_year: int, end_year: int):
    return get_latest_grades(tckr, start_year, end_year)
