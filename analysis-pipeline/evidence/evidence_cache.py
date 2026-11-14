from datetime import datetime, timezone

from evidence.instructions import BASE_VERSION
from evidence.types import EvidenceResponse
from utils import llm
from utils.dynamo import evidence_table

# Combines the base-instructions version with the question's own version, so
# bumping either invalidates evidence produced by the old prompt.
def version_tag(question: dict) -> str:
    return f"{BASE_VERSION}-{question['version']}"

# Leading "{qid}#" lets reads query by prefix per question.
def key_prefix(qid: str) -> str:
    return f"{qid}#"

# Identifies which filing block / question / prompt / model version produced
# (or would produce) the evidence, so a prompt edit or model swap never serves
# stale evidence. 10-K blocks have no quarter, so "FY" fills that slot to keep
# the segment positions consistent with 10-Q blocks.
def _key(question: dict, block: dict) -> str:
    return "#".join([
        question["id"],
        block["year"], block["form"], block.get("quarter", "FY"),
        version_tag(question), llm.MODEL_ID,
    ])

# Returns None on a cache miss.
def get_cached(tckr: str, question: dict, block: dict) -> EvidenceResponse | None:
    item = evidence_table.get(tckr, _key(question, block))
    return EvidenceResponse.model_validate_json(item["evidence_json"]) if item else None

# Persists evidence so future runs of this exact block/question/version skip the LLM call.
def store(tckr: str, question: dict, block: dict, evidence: EvidenceResponse) -> None:
    evidence_table.put(
        tckr,
        _key(question, block),
        year=block["year"],
        form=block["form"],
        quarter=block.get("quarter", "FY"),
        section=block["section"],
        evidence_json=evidence.model_dump_json(),
        created_at=datetime.now(timezone.utc).isoformat(),
    )
