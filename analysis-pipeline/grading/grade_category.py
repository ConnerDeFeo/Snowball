from grading.types.GradedTimePeriod import GradedTimePeriod
from enums.RubricCategory import RubricCategory
from grading.constants.rubric_directions import RUBRIC_DIRECTIONS
from grading.fetch_sections import fetch_sections
from grading.grade_prompt import build_prompt, invoke_bedrock

def grade_category(tckr:str, rubric_category: RubricCategory, start_date:str, end_date:str) -> GradedTimePeriod:
    category_meta = RUBRIC_DIRECTIONS[rubric_category]
    sections = fetch_sections(tckr, start_date, end_date, category_meta["locations"])

    prompt = build_prompt(category_meta, sections)
    result = invoke_bedrock(prompt)

    return GradedTimePeriod(
        category=rubric_category,
        start=start_date,
        end=end_date,
        grade=result["grade"],
        reasoning=result["reasoning"],
        quotes=result["quotes"],
    )