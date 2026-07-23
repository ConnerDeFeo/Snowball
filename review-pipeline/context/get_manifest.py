from utils.dynamo import section_grades_table, findings_table
from utils.finding_key import split_key, version_sort_key

def get_findings_manifest(tckr: str, start_year: int, end_year: int) -> str:
    items = findings_table.query_range(tckr, f"{start_year}#", f"{end_year}$")

    latest_by_filing_section: dict[str, dict] = {}
    for item in items:
        key = item["finding_key"]
        filing_section = "#".join(split_key(key)[:5])
        current = latest_by_filing_section.get(filing_section)
        if current is None or version_sort_key(key) > version_sort_key(current["finding_key"]):
            latest_by_filing_section[filing_section] = item

    groups: dict[tuple[str, str, str], list[str]] = {}
    for item in latest_by_filing_section.values():
        year, form, period, category, section, *_ = split_key(item["finding_key"])
        groups.setdefault((year, form, period), []).append(f"{category} / {section}")

    lines = []
    for (year, form, period) in sorted(groups):
        lines.append(f"{year} | {form} | {period}")
        for entry in sorted(groups[(year, form, period)]):
            lines.append(f"  {entry}")
    return "\n".join(lines)

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
