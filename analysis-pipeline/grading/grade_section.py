import asyncio
import json
from typing import Awaitable, Callable, Optional

from document_retrieval.FormType import FormType
from grading.enums.RubricCategory import RubricCategory
from grading.enums.Sections import TenKSection, TenQSection
from grading.constants.rubric_directions import BASE_INSTRUCTIONS, RUBRIC_DIRECTIONS
from grading.extract_findings import extract_findings
from grading.fetch_sections import fetch_sections
from grading import finding_cache
from grading import grade_store
from grading.types.GradedTimePeriod import GradedTimePeriod
from grading.types.SectionMeta import SectionMeta
from utils import bedrock

MAX_WORKERS = 8  # cap concurrent Bedrock sub-agent calls per grade_section run

# Fallback result used whenever there's nothing to grade (no rubric yet, or no
# cached filings) so grade_section never has to raise or return None.
def _no_evidence(rubric_category: RubricCategory, start_date: str, end_date: str, reasoning: str) -> GradedTimePeriod:
    return GradedTimePeriod(
        category=rubric_category, 
        start=start_date, 
        end=end_date,
        grade=0.0, 
        reasoning=reasoning, 
        quotes=[],
    )

# TenKSection/TenQSection share string values, so the block's form type
# decides which enum a given section string belongs to.
def _section_enum(form: str, section: str) -> TenKSection | TenQSection:
    if form == FormType.TEN_K.value:
        return TenKSection(section)
    return TenQSection(section)

# Runs the per-section sub-agent (extract_findings) on one fetched block and
# packages the result as a SectionMeta. Called in parallel, once per block.
# Checks the findings cache first so a previously graded block/category/section
# (same prompt + model version) never re-triggers the Bedrock call.
def _to_section_meta(tckr: str, block: dict, rubric_category: RubricCategory) -> SectionMeta:
    section = _section_enum(block["form"], block["section"])
    findings = finding_cache.get_cached(tckr, block, rubric_category, section)
    if findings is None:
        findings = extract_findings(block["text"], rubric_category, section)
        finding_cache.store(tckr, block, rubric_category, section, findings)
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
def _label_section_meta(block: dict, meta: SectionMeta) -> dict:
    label = {"form": block["form"], "year": block["year"], "section": block["section"]}
    if "quarter" in block:
        label["quarter"] = block["quarter"]
    label["findings"] = meta.model_dump(mode="json")
    return label

async def grade_section(
    tckr: str,
    start_date: str,
    end_date: str,
    rubric_category: RubricCategory,
    # Callable function that takes dict param and returns awaitable nothing
    on_progress: Optional[Callable[[dict], Awaitable[None]]] = None,
) -> GradedTimePeriod:
    # 1. Look up where to look (section locations) and what to look for
    # (directions) for this rubric category.
    cfg = RUBRIC_DIRECTIONS.get(rubric_category)
    if cfg is None:
        return _no_evidence(rubric_category, start_date, end_date, "No rubric directions defined yet for this category.")

    # 2. Pull the cached filing text for those locations within the date window.
    blocks = await asyncio.to_thread(fetch_sections, tckr, start_date, end_date, cfg["locations"])
    if not blocks:
        return _no_evidence(rubric_category, start_date, end_date, "No cached filings found for this ticker/period.")

    total = len(blocks)
    if on_progress:
        await on_progress({"type": "start", "total": total})

    # 3. Extract findings from each filing section in parallel — each call is
    # an independent, blocking Bedrock request, so threads overlap the I/O wait.
    # gather (not as_completed) keeps `metas` in `blocks` order for the zip below,
    # while each _run still reports progress as soon as its own block finishes.
    sem = asyncio.Semaphore(MAX_WORKERS)
    completed = 0

    async def _run(block: dict) -> SectionMeta:
        nonlocal completed
        async with sem:
            meta = await asyncio.to_thread(_to_section_meta, tckr, block, rubric_category)
        if on_progress:
            completed += 1
            await on_progress({
                "type": "progress",
                "completed": completed,
                "total": total,
                "form": block["form"],
                "year": block["year"],
                "section": block["section"],
                "quarter": block.get("quarter"),
            })
        return meta

    metas = await asyncio.gather(*[_run(block) for block in blocks])

    # 4. Label each section's findings with its filing metadata (form/year/
    # quarter) so the final grader can see how evidence is distributed over time.
    labeled = [_label_section_meta(block, meta) for block, meta in zip(blocks, metas)]

    # 5. Hand all the labeled findings to one final grading call, which scores
    # the whole category/period based on the aggregated evidence.
    user_prompt = f"""
      Category: {cfg["name"]}
      Directions: {cfg["directions"]}

      Findings by filing:
      {json.dumps(labeled, indent=2)}
    """

    response = await asyncio.to_thread(bedrock.invoke, BASE_INSTRUCTIONS, user_prompt)
    parsed = json.loads(response)

    graded = GradedTimePeriod(
        category=rubric_category,
        start=start_date,
        end=end_date,
        grade=float(parsed["grade"]),
        reasoning=parsed["reasoning"],
        quotes=parsed["quotes"],
    )

    # Persist the graded result so it can be looked up later without re-grading.
    await asyncio.to_thread(grade_store.store, tckr, graded)
    return graded
