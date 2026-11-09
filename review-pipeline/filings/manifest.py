from utils.s3 import list_keys

# Lists the cached 10-K/10-Q sections for the ticker within [start_year, end_year],
# grouped by filing, so the agent knows what it can read.
def filings_manifest(tckr: str, start_year: int, end_year: int) -> str:
    groups: dict[tuple[str, str, str], list[str]] = {}
    for form in ("10-K", "10-Q"):
        prefix = f"filings/{tckr}/{form}/"
        for key in list_keys(prefix):
            parts = key[len(prefix):].split("/")  # [year, section.txt] or [year, quarter, section.txt]
            if not parts[-1].endswith(".txt") or not start_year <= int(parts[0]) <= end_year:
                continue
            quarter = parts[1] if len(parts) == 3 else "FY"
            groups.setdefault((parts[0], form, quarter), []).append(parts[-1].removesuffix(".txt"))

    lines = []
    for year, form, quarter in sorted(groups):
        lines.append(f"{year} | {form} | {quarter}")
        lines += [f"  {section}" for section in sorted(groups[(year, form, quarter)])]
    return "\n".join(lines)
