from grading.enums.RubricCategory import RubricCategory
from grading.enums.Sections import Section
from grading.constants.rubric_directions import (
    resolve_sub_agent_direction,
    sub_agent_prompt_version,
)
from grading.extract_findings import FindingsResponse
from utils import bedrock
from utils.dynamo import findings_table

# Identifies which filing block/category/section/prompt/model version produced
# (or would produce) the findings, so a rubric change, prompt edit, or model
# swap never serves stale cached findings. 10-K blocks have no quarter, so "FY"
# fills that slot to keep the segment positions consistent with 10-Q blocks.
def _finding_key(block: dict, rubric_category: RubricCategory, section: Section) -> str:
    direction = resolve_sub_agent_direction(rubric_category, section)
    quarter = block.get("quarter", "FY")
    return "#".join([
        block["year"], block["form"], quarter,
        rubric_category.value, section.value,
        sub_agent_prompt_version(direction), bedrock.MODEL_ID,
    ])

# Looks up previously cached findings for this exact block/category/section,
# under the current prompt + model version. Returns None on a cache miss.
def get_cached(tckr: str, block: dict, rubric_category: RubricCategory, section: Section) -> FindingsResponse | None:
    item = findings_table.get(tckr, _finding_key(block, rubric_category, section))
    return FindingsResponse.model_validate_json(item["findings_json"]) if item else None

# Persists sub-agent findings so future lookups for this exact block/category/
# section/version can skip the Bedrock call entirely.
def store(tckr: str, block: dict, rubric_category: RubricCategory, section: Section, findings: FindingsResponse) -> None:
    findings_table.put(
        tckr,
        _finding_key(block, rubric_category, section),
        findings_json=findings.model_dump_json(),
    )
