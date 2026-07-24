from grading.enums.RubricCategory import RubricCategory
from grading.enums.Sections import Section
from grading.rubric_directions import sub_agent_prompt_version
from grading.extract_findings import FindingsResponse
from utils import bedrock
from utils.dynamo import findings_table

# Identifies which filing block/category/section/prompt/model version produced
# (or would produce) the findings, so a rubric change, prompt edit, or model
# swap never serves stale cached findings. `direction` is the already-resolved
# sub-agent direction for this rubric_category/section (caller and cache must
# agree on which one was used). 10-K blocks have no quarter, so "FY" fills that
# slot to keep the segment positions consistent with 10-Q blocks.
def _finding_key(block: dict, rubric_category: RubricCategory, section: Section, direction: dict) -> str:
    quarter = block.get("quarter", "FY")
    return "#".join([
        block["year"], block["form"], quarter,
        rubric_category.value, section.value,
        sub_agent_prompt_version(direction), bedrock.MODEL_ID,
    ])

# Looks up previously cached findings for this exact block/category/section,
# under the current prompt + model version. Returns None on a cache miss.
def get_cached(tckr: str, block: dict, rubric_category: RubricCategory, section: Section, direction: dict) -> FindingsResponse | None:
    item = findings_table.get(tckr, _finding_key(block, rubric_category, section, direction))
    return FindingsResponse.model_validate_json(item["findings_json"]) if item else None

# Persists sub-agent findings so future lookups for this exact block/category/
# section/version can skip the Bedrock call entirely.
def store(tckr: str, block: dict, rubric_category: RubricCategory, section: Section, direction: dict, findings: FindingsResponse) -> None:
    findings_table.put(
        tckr,
        _finding_key(block, rubric_category, section, direction),
        findings_json=findings.model_dump_json(),
    )
