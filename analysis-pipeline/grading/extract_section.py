from enums.FormType import FormType
from enums.RubricCategory import RubricCategory
from enums.Sections import section_from_form
from grading.rubric_directions import resolve_sub_agent_direction
from grading.extract_findings import extract_findings
from grading import finding_cache
from grading.types.SectionMeta import SectionMeta

# Get the section information that is needed for the rubric category
def extract_section_meta(tckr: str, block: dict, rubric_category: RubricCategory, cfg: dict) -> SectionMeta:
    section = section_from_form(block["form"], block["section"])
    direction = resolve_sub_agent_direction(cfg, block["form"], section)
    findings = finding_cache.get_cached(tckr, block, rubric_category, section, direction)
    # If already extracted, just reutrn cached
    if findings is None:
        block_label = f"{tckr}/{block['form']}/{block['year']}" + (f"Q{block['quarter']}" if "quarter" in block else "") + f"/{block['section']}"
        findings = extract_findings(block["text"], rubric_category, section, direction, block_label=block_label)
        finding_cache.store(tckr, block, rubric_category, section, direction, findings)
    return SectionMeta(
        filing_type=FormType(block["form"]),
        section=section,
        rubric_category=rubric_category,
        finding=findings.findings,
        notable_anomalies=findings.notable_anomalies,
        section_present=True,  # fetch_sections only returns sections that exist
    )

# Attaches the filing label (form/year/quarter) fetch_sections already knew
# onto the SectionMeta's findings, so the final grader prompt can cite dates.
def label_section_meta(block: dict, meta: SectionMeta) -> dict:
    label = {"form": block["form"], "year": block["year"], "section": block["section"]}
    if "quarter" in block:
        label["quarter"] = block["quarter"]
    label["findings"] = meta.model_dump(mode="json")
    return label
