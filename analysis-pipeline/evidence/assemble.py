from evidence.plan_work import sort_key
from evidence.types import EvidenceResponse

# One piece of evidence from one filing, tagged with the question it answers.
def entry(qid: str, form: str, year: str, quarter: str | None, section: str, evidence: EvidenceResponse) -> dict:
    return {
        "qid": qid, "form": form, "year": year, "quarter": quarter, "section": section,
        "findings": [f.model_dump() for f in evidence.findings],    }

# Nests flat entries under the checklist: category -> question -> evidence.
# Questions with no evidence still appear, with an empty list.
def build(categories: list[dict], entries: list[dict]) -> list[dict]:
    by_question: dict[str, list[dict]] = {}
    for e in entries:
        by_question.setdefault(e["qid"], []).append({k: v for k, v in e.items() if k != "qid"})

    return [
        {
            "id": c["id"], "name": c["name"],
            "questions": [
                {
                    "id": q["id"], "text": q["text"], "form": q["form"], "section": q["section"],
                    "latest_only": q["latest_only"],
                    "evidence": sorted(by_question.get(q["id"], []), key=lambda e: sort_key(e["year"], e["quarter"])),
                }
                for q in c["questions"]
            ],
        }
        for c in categories
    ]
