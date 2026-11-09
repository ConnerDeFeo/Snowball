from enums.Sections import Section, section_from_form

# Orders filings chronologically: year first, then quarter ("FY"/None sorts as
# the annual filing within its year).
def sort_key(year: str | int, quarter: str | None) -> tuple:
    return (int(year), quarter or "")

# Every distinct section the selected sub-agents point at, so a run fetches each
# one from S3 once instead of once per sub-agent.
def locations(categories: list[dict]) -> list[Section]:
    return list({
        section_from_form(sa["form"], sa["section"])
        for c in categories for q in c["questions"] for sa in q["sub_agents"]
    })

# Pairs each sub-agent with the fetched blocks it targets (same form + section).
# A `latest_only` question only gets the most recent matching filing.
def plan(categories: list[dict], blocks: list[dict]) -> list[dict]:
    by_target: dict[tuple, list[dict]] = {}
    for block in blocks:
        by_target.setdefault((block["form"], block["section"]), []).append(block)

    work = []
    for c in categories:
        for q in c["questions"]:
            for sa in q["sub_agents"]:
                matches = by_target.get((sa["form"], sa["section"]), [])
                if q["latest_only"] and matches:
                    matches = [max(matches, key=lambda b: sort_key(b["year"], b.get("quarter")))]
                work += [{"question": q, "sub_agent": sa, "block": b} for b in matches]
    return work
