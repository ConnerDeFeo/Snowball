from pydantic import BaseModel

from enums.RubricCategory import RubricCategory

class GradedTimePeriod(BaseModel):
    category: RubricCategory
    start: int
    end: int
    grade: float
    reasoning: str
    quotes: list[str]