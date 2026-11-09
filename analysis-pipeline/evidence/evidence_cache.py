from datetime import datetime, timezone

from evidence.instructions import BASE_VERSION
from evidence.types import EvidenceResponse
from utils import bedrock
from utils.dynamo import evidence_table

# Combines the base-instructions version with the sub-agent's own version, so
# bumping either invalidates evidence produced by the old prompt.
def version_tag(sub_agent: dict) -> str:
    return f"{BASE_VERSION}-{sub_agent['version']}"

# Leading "{qid}#" / "{qid}#{said}#" lets reads query by prefix per question
# or per sub-agent.
def key_prefix(qid: str, said: str = "") -> str:
    return f"{qid}#{said}#" if said else f"{qid}#"

# Identifies which filing block / sub-agent / prompt / model version produced
# (or would produce) the evidence, so a prompt edit or model swap never serves
# stale evidence. 10-K blocks have no quarter, so "FY" fills that slot to keep
# the segment positions consistent with 10-Q blocks.
def _key(question: dict, sub_agent: dict, block: dict) -> str:
    return "#".join([
        question["id"], sub_agent["id"],
        block["year"], block["form"], block.get("quarter", "FY"),
        version_tag(sub_agent), bedrock.MODEL_ID,
    ])

# Returns None on a cache miss.
def get_cached(tckr: str, question: dict, sub_agent: dict, block: dict) -> EvidenceResponse | None:
    item = evidence_table.get(tckr, _key(question, sub_agent, block))
    return EvidenceResponse.model_validate_json(item["evidence_json"]) if item else None

# Persists evidence so future runs of this exact block/sub-agent/version skip Bedrock.
def store(tckr: str, question: dict, sub_agent: dict, block: dict, evidence: EvidenceResponse) -> None:
    evidence_table.put(
        tckr,
        _key(question, sub_agent, block),
        year=block["year"],
        form=block["form"],
        quarter=block.get("quarter", "FY"),
        section=block["section"],
        evidence_json=evidence.model_dump_json(),
        created_at=datetime.now(timezone.utc).isoformat(),
    )
