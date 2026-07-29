from enums.RubricCategory import RubricCategory
from grading.types.GradedTimePeriod import GradedTimePeriod
from utils.dynamo import section_grades_table

# Reads back previously graded results for a ticker/year-range, keeping only
# the latest rubric-version per category (an edited rubric bumps its META
# version and leaves the old grade row in place rather than overwriting it).
def get_latest_grades(tckr: str, start_year: int, end_year: int) -> list[GradedTimePeriod]:
    prefix = f"{start_year}#{end_year}#"
    items = section_grades_table.query(tckr, prefix)

    latest_by_category: dict[str, dict] = {}
    for item in items:
        category = item["category_period"].split("#")[2]
        current = latest_by_category.get(category)
        if current is None or (
            section_grades_table.version_sort_key(item["category_period"])
            > section_grades_table.version_sort_key(current["category_period"])
        ):
            latest_by_category[category] = item

    return [
        GradedTimePeriod(
            category=RubricCategory(category),
            start=start_year,
            end=end_year,
            grade=float(item["grade"]),
            reasoning=item["reasoning"],
            quotes=item["quotes"],
        )
        for category, item in sorted(latest_by_category.items())
    ]
