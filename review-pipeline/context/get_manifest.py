from utils.dynamo import section_grades_table

def get_manifest(tckr: str, start_date: str, end_date: str) -> list[dict]:
    prefix = f"{start_date}#{end_date}#"
    items = section_grades_table.query(tckr, prefix)
    manifest = [
        {
            "rubric_category": item["category_period"].split("#")[-1],
            "grade": item["grade"],
        }
        for item in items
    ]
    return "\n".join(f"{section}: {score}" for section, score in manifest.items())
