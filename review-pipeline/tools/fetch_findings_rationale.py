# tools/fetch_findings_rationale.py
from utils.dynamo import findings_table
from utils.finding_key import version_sort_key

def fetch_findings_rationale(tckr: str, year: str, form: str, period: str, rubric_category: str, section: str) -> dict | None:
    rubric_category = rubric_category.lower()
    section = section.lower()
    prefix = f"{year}#{form}#{period}#{rubric_category}#{section}#"
    items = findings_table.query_prefix(tckr, prefix)
    if not items:
        return None
    return max(items, key=lambda item: version_sort_key(item["finding_key"]))
