from pydantic import BaseModel

from grading.enums.RubricCategory import RubricCategory

class GradedTimePeriod(BaseModel):
    category: RubricCategory
    start: int
    end: int
    grade: float
    reasoning: str
    quotes: list[str]