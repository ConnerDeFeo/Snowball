from utils.dynamo import section_grades_table

def fetch_rationale(tckr: str, start: str, end: str, rubric_category: str) -> dict | None:
    category_period = f"{start}#{end}#{rubric_category}"
    return section_grades_table.get(tckr, category_period)
