from concurrent.futures import ThreadPoolExecutor

from checklist import load
from evidence import assemble, evidence_cache
from evidence.plan_work import sort_key
from evidence.types import EvidenceResponse
from utils import bedrock
from utils.dynamo import evidence_table

# Reads already-stored evidence without calling Bedrock. Only evidence produced
# under the current prompt + model versions counts, so an edited question
# shows no evidence until it is re-run.
def read_evidence(tckr: str, start_year: int, end_year: int, category_id: str | None = None, question_id: str | None = None) -> list[dict]:
    categories = load.select(category_id, question_id)
    questions = [q for c in categories for q in c["questions"]]

    # One query per question (prefix "{qid}#"), run in parallel.
    with ThreadPoolExecutor(max_workers=8) as pool:
        stored = list(pool.map(lambda q: evidence_table.query_prefix(tckr, evidence_cache.key_prefix(q["id"])), questions))

    entries = []
    for q, items in zip(questions, stored):
        kept = []
        for item in items:
            # key: qid#year#form#quarter#version#model
            _, _, _, _, version, model = item["evidence_key"].split("#")
            if model != bedrock.MODEL_ID or version != evidence_cache.version_tag(q):
                continue
            if start_year <= int(item["year"]) <= end_year:
                kept.append(item)

        if q["latest_only"] and kept:
            kept = [max(kept, key=lambda i: sort_key(i["year"], None if i["quarter"] == "FY" else i["quarter"]))]
        for i in kept:
            entries.append(assemble.entry(
                q["id"], i["form"], i["year"], None if i["quarter"] == "FY" else i["quarter"], i["section"],
                EvidenceResponse.model_validate_json(i["evidence_json"]),
            ))
    return assemble.build(categories, entries)
