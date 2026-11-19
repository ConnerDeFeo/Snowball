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

    # Proxies have no sections: one line each, with the id the proxy tools take.
    proxy_prefix = f"filings/{tckr}/DEF 14A/"
    proxy_ids = sorted(
        key[len(proxy_prefix):].split("/")[0]
        for key in list_keys(proxy_prefix)
        if key.endswith("/proxy.txt") and start_year <= int(key[len(proxy_prefix):][:4]) <= end_year
    )
    lines += [f"{proxy_id[:4]} | DEF 14A | {proxy_id}" for proxy_id in proxy_ids]
    return "\n".join(lines)
