from utils.dynamo import section_grades_table

def fetch_grade_rationale(tckr: str, start: int, end: int, rubric_category: str) -> dict | None:
    rubric_category = rubric_category.lower()
    category_period = f"{start}#{end}#{rubric_category}"
    return section_grades_table.get(tckr, category_period)
