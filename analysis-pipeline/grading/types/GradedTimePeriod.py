from typing import NamedTuple

from enums.RubricCategory import RubricCategory

class GradedTimePeriod(NamedTuple):
    category: RubricCategory
    start: str
    end: str
    grade: float
    reasoning: str
    quotes: list[str]