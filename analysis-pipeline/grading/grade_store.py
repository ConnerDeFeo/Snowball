from datetime import datetime, timezone
from decimal import Decimal

from enums.RubricCategory import RubricCategory
from grading.types.GradedTimePeriod import GradedTimePeriod
from utils.dynamo import section_grades_table

# Identifies which category/period/rubric-version this graded result covers,
# under one ticker. The rubric version is included so editing a rubric (which
# bumps its META version) invalidates the old grade instead of serving it
# stale — old-version rows are left in the table rather than overwritten.
def _category_period(start: int, end: int, category: RubricCategory, version: str) -> str:
    return f"{start}#{end}#{category.value}#{version}"

# Looks up a previously graded time period so grade_section can skip re-running
# the pipeline. Returns None on a cache miss.
def load(tckr: str, start: int, end: int, category: RubricCategory, version: str) -> GradedTimePeriod | None:
    item = section_grades_table.get(tckr, _category_period(start, end, category, version))
    if item is None:
        return None
    return GradedTimePeriod(
        category=category,
        start=start,
        end=end,
        grade=float(item["grade"]),
        reasoning=item["reasoning"],
        quotes=item["quotes"],
    )

# Persists a graded time period so it can be looked up later without re-running
# the grading pipeline. grade is stored as Decimal since the boto3 DynamoDB
# resource rejects Python floats.
def store(tckr: str, graded: GradedTimePeriod, version: str) -> None:
    section_grades_table.put(
        tckr,
        _category_period(graded.start, graded.end, graded.category, version),
        grade=Decimal(str(graded.grade)),
        reasoning=graded.reasoning,
        quotes=graded.quotes,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
