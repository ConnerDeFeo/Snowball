from utils.dynamo import section_grades_table, findings_table, split_key

def get_findings_manifest(tckr: str, start_year: int, end_year: int) -> str:
    """List each filing's sections, keeping only the latest version of each finding."""
    items = findings_table.query_range(tckr, f"{start_year}#", f"{end_year}$")

    # Dedupe: for each filing+section, keep only the highest-versioned finding.
    latest_by_filing_section: dict[str, dict] = {}
    for item in items:
        key = item["finding_key"]
        filing_section = "#".join(split_key.split_key(key)[:5])
        current = latest_by_filing_section.get(filing_section)
        if current is None or findings_table.version_sort_key(key) > findings_table.version_sort_key(current["finding_key"]):
            latest_by_filing_section[filing_section] = item

    # Group surviving findings by filing (year/form/period).
    groups: dict[tuple[str, str, str], list[str]] = {}
    for item in latest_by_filing_section.values():
        year, form, period, category, section, *_ = split_key.split_key(item["finding_key"])
        groups.setdefault((year, form, period), []).append(f"{category} / {section}")

    # Render as a nested text manifest, one filing header per group.
    lines = []
    for (year, form, period) in sorted(groups):
        lines.append(f"{year} | {form} | {period}")
        for entry in sorted(groups[(year, form, period)]):
            lines.append(f"  {entry}")
    return "\n".join(lines)

def get_grade_manifest(tckr: str, start_year: int, end_year: int) -> str:
    """List each rubric category's grade for the given ticker/year range, keeping
    only the latest version of each grade (a rubric edit bumps the version and
    leaves the old row in place, so without this the same category would show
    up once per version)."""
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

    return "\n".join(
        f"{category}: {item['grade']}"
        for category, item in sorted(latest_by_category.items())
    )
