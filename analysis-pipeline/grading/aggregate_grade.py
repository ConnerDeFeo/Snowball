import json

from pydantic import BaseModel

from enums.RubricCategory import RubricCategory
from grading.rubric_directions import BASE_INSTRUCTIONS
from grading import grade_store
from grading.parse_response import invoke_parsed
from grading.types.GradedTimePeriod import GradedTimePeriod
from utils import bedrock

class AggregateResponse(BaseModel):
    grade: float
    reasoning: str
    quotes: list[str]

# Fallback result used whenever there's nothing to grade (no rubric yet, or no
# cached filings) so a caller never has to raise or return None.
def no_evidence(rubric_category: RubricCategory, start_year: int, end_year: int, reasoning: str) -> GradedTimePeriod:
    return GradedTimePeriod(
        category=rubric_category,
        start=start_year,
        end=end_year,
        grade=0.0,
        reasoning=reasoning,
        quotes=[],
    )

# Hands all the labeled per-block findings for one category to one final
# grading call, which scores the whole category/period based on the
# aggregated evidence, then persists the result so it can be looked up later
# without re-grading.
def aggregate_grade(
    tckr: str,
    rubric_category: RubricCategory,
    cfg: dict,
    labeled: list[dict],
    start_year: int,
    end_year: int,
) -> GradedTimePeriod:
    user_prompt = f"""
      Category: {cfg["name"]}
      Directions: {cfg["directions"]}

      Findings by filing:
      {json.dumps(labeled, indent=2)}
    """

    label = f"tckr={tckr} category={rubric_category.value}"
    parsed = invoke_parsed(lambda: bedrock.invoke(BASE_INSTRUCTIONS, user_prompt), AggregateResponse, label=label)

    graded = GradedTimePeriod(
        category=rubric_category,
        start=start_year,
        end=end_year,
        grade=parsed.grade,
        reasoning=parsed.reasoning,
        quotes=parsed.quotes,
    )

    grade_store.store(tckr, graded, cfg["version"])
    return graded
