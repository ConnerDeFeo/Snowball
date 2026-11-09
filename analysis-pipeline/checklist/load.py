# Reads a category's partition (META + questions + sub-agents) and shapes it
# into nested dicts. Queried fresh every call (no caching) so an edit is
# picked up on the very next run, without a redeploy.
from fastapi import HTTPException

from checklist.keys import META_SK
from utils.dynamo import checklist_table


def _shape_sub_agent(item: dict) -> dict:
    return {"id": item["sk"].split("#SA#")[1], "form": item["form"], "section": item["section"],
            "prompt": item["prompt"], "version": item["version"]}


def _shape(category_id: str, items: list[dict]) -> dict | None:
    meta = next((i for i in items if i["sk"] == META_SK), None)
    if meta is None:
        return None
    questions = []
    for q in (i for i in items if i["sk"].startswith("Q#") and "#SA#" not in i["sk"]):
        qid = q["sk"].removeprefix("Q#")
        subs = [i for i in items if i["sk"].startswith(f"Q#{qid}#SA#")]
        questions.append({
            "id": qid, "text": q["text"], "order": int(q["order"]),
            "latest_only": q["latest_only"], "version": q["version"],
            "sub_agents": sorted((_shape_sub_agent(s) for s in subs), key=lambda s: s["id"]),
        })
    questions.sort(key=lambda q: (q["order"], q["id"]))
    return {"id": category_id, "name": meta["name"], "order": int(meta["order"]), "questions": questions}


def get_category(category_id: str) -> dict:
    shaped = _shape(category_id, checklist_table.query_category(category_id))
    if shaped is None:
        raise HTTPException(status_code=404, detail=f"category {category_id} not found")
    return shaped


def get_all() -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for item in checklist_table.scan_all():
        grouped.setdefault(item["category_id"], []).append(item)
    shaped = (_shape(cid, items) for cid, items in grouped.items())
    return sorted((s for s in shaped if s is not None), key=lambda s: (s["order"], s["id"]))


# Narrows the loaded checklist to one category and/or one question for a run.
def select(category_id: str | None = None, question_id: str | None = None) -> list[dict]:
    categories = [get_category(category_id)] if category_id else get_all()
    if question_id:
        for c in categories:
            c["questions"] = [q for q in c["questions"] if q["id"] == question_id]
        categories = [c for c in categories if c["questions"]]
        if not categories:
            raise HTTPException(status_code=404, detail=f"question {question_id} not found")
    return categories
