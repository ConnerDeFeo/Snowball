from utils.dynamo import section_grades_table

def fetch_grade_rationale(tckr: str, start: int, end: int, rubric_category: str) -> dict | None:
    rubric_category = rubric_category.lower()
    prefix = f"{start}#{end}#{rubric_category}#"
    items = section_grades_table.query(tckr, prefix)
    if not items:
        return None
    return max(items, key=lambda item: section_grades_table.version_sort_key(item["category_period"]))
