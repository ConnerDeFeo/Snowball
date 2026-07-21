from datetime import datetime, timezone
from decimal import Decimal

from grading.types.GradedTimePeriod import GradedTimePeriod
from utils import section_grades_table

# Identifies which category/period this graded result covers, under one ticker.
def _category_period(graded: GradedTimePeriod) -> str:
    return f"{graded.start}-{graded.end}#{graded.category.value}"

# Persists a graded time period so it can be looked up later without re-running
# the grading pipeline. grade is stored as Decimal since the boto3 DynamoDB
# resource rejects Python floats.
def store(tckr: str, graded: GradedTimePeriod) -> None:
    section_grades_table.put(
        tckr,
        _category_period(graded),
        grade=Decimal(str(graded.grade)),
        reasoning=graded.reasoning,
        quotes=graded.quotes,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
