from enums.RubricCategory import RubricCategory
from grading.types.GradedTimePeriod import GradedTimePeriod

def grade_section(tckr: str, start_date:str, end_date:str, rubric_category:RubricCategory) -> GradedTimePeriod:
    return