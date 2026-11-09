from evidence.plan_work import sort_key
from evidence.types import EvidenceResponse

# One piece of evidence from one filing, tagged with the sub-agent that found it.
def entry(said: str, form: str, year: str, quarter: str | None, section: str, evidence: EvidenceResponse) -> dict:
    return {
        "said": said, "form": form, "year": year, "quarter": quarter, "section": section,
        "findings": [f.model_dump() for f in evidence.findings],
        "summary": evidence.summary,
    }

# Nests flat entries under the checklist: category -> question -> sub-agent -> evidence.
# Sub-agents with no evidence still appear, with an empty list.
def build(categories: list[dict], entries: list[dict]) -> list[dict]:
    by_agent: dict[str, list[dict]] = {}
    for e in entries:
        by_agent.setdefault(e["said"], []).append({k: v for k, v in e.items() if k != "said"})

    return [
        {
            "id": c["id"], "name": c["name"],
            "questions": [
                {
                    "id": q["id"], "text": q["text"], "latest_only": q["latest_only"],
                    "sub_agents": [
                        {
                            "id": sa["id"], "form": sa["form"], "section": sa["section"],
                            "evidence": sorted(by_agent.get(sa["id"], []), key=lambda e: sort_key(e["year"], e["quarter"])),
                        }
                        for sa in q["sub_agents"]
                    ],
                }
                for q in c["questions"]
            ],
        }
        for c in categories
    ]
