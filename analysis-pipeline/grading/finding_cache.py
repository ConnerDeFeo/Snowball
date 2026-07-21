from grading.enums.RubricCategory import RubricCategory
from grading.enums.Sections import Section
from grading.constants.rubric_directions import (
    resolve_sub_agent_direction,
    sub_agent_prompt_version,
)
from grading.extract_findings import FindingsResponse
from utils import bedrock
from utils.dynamo import findings_table

# Identifies which filing section/category this sub-agent call is about.
# Quarter is only present on 10-Q blocks, so it's only included then.
def _section_key(tckr: str, block: dict, rubric_category: RubricCategory, section: Section) -> str:
    parts = [tckr, block["form"], block["year"]]
    if "quarter" in block:
        parts.append(block["quarter"])
    parts += [rubric_category.value, section.value]
    return "#".join(parts)

# Identifies which prompt + model version produced (or would produce) the
# findings, so a prompt edit or model swap never serves stale cached findings.
def _version_key(rubric_category: RubricCategory, section: Section) -> str:
    direction = resolve_sub_agent_direction(rubric_category, section)
    return f"{sub_agent_prompt_version(direction)}#{bedrock.MODEL_ID}"

# Looks up previously cached findings for this exact block/category/section,
# under the current prompt + model version. Returns None on a cache miss.
def get_cached(tckr: str, block: dict, rubric_category: RubricCategory, section: Section) -> FindingsResponse | None:
    item = findings_table.get(
        _section_key(tckr, block, rubric_category, section),
        _version_key(rubric_category, section),
    )
    return FindingsResponse.model_validate_json(item["findings_json"]) if item else None

# Persists sub-agent findings so future lookups for this exact block/category/
# section/version can skip the Bedrock call entirely.
def store(tckr: str, block: dict, rubric_category: RubricCategory, section: Section, findings: FindingsResponse) -> None:
    findings_table.put(
        _section_key(tckr, block, rubric_category, section),
        _version_key(rubric_category, section),
        findings_json=findings.model_dump_json(),
    )
