from utils.dynamo import section_grades_table

def get_findings_manifest():
    pass

def get_grade_manifest(tckr: str, start_year: int, end_year: int) -> str:
    prefix = f"{start_year}#{end_year}#"
    items = section_grades_table.query(tckr, prefix)
    manifest = [
        {
            "rubric_category": item["category_period"].split("#")[-1],
            "grade": item["grade"],
        }
        for item in items
    ]
    return "\n".join(f"{item['rubric_category']}: {item['grade']}" for item in manifest)
