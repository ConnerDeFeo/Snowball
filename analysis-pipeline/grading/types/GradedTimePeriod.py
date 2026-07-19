from typing import NamedTuple

class GradedTimePeriod(NamedTuple):
    start: str
    end: str
    grade: float
    reasoning: str
    quotes: list[str]