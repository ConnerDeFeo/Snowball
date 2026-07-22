from utils.dynamo import section_grades_table

def get_manifest(tckr: str, start_date: str, end_date: str) -> str:
    prefix = f"{start_date}#{end_date}#"
    items = section_grades_table.query(tckr, prefix)
    manifest = [
        {
            "rubric_category": item["category_period"].split("#")[-1],
            "grade": item["grade"],
        }
        for item in items
    ]
    return "\n".join(f"{item['rubric_category']}: {item['grade']}" for item in manifest)
