from pydantic import BaseModel

from enums.RubricCategory import RubricCategory

class GradedTimePeriod(BaseModel):
    category: RubricCategory
    start: str
    end: str
    grade: float
    reasoning: str
    quotes: list[str]