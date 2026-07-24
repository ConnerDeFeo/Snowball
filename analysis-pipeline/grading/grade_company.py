import asyncio
from typing import Awaitable, Callable, Optional

from enums.RubricCategory import RubricCategory
from enums.Sections import section_from_form
from grading.rubric_directions import get_rubric_directions
from grading.extract_section import extract_section_meta, label_section_meta
from grading.aggregate_grade import aggregate_grade, no_evidence
from grading.fetch_sections import fetch_sections
from grading import grade_store
from grading.types.GradedTimePeriod import GradedTimePeriod
from grading.types.SectionMeta import SectionMeta

MAX_WORKERS = 8  # cap concurrent Bedrock sub-agent calls per block, same as grade_section

# Grades every configured rubric category for one ticker/period in one run.
# Fetches each unique filing section once (instead of once per category) and
# runs categories that share a section back-to-back, so Bedrock prompt
# caching (see extract_findings) only pays to process that section's text
# once per block instead of once per category.
async def grade_company(
    tckr: str,
    start_year: int,
    end_year: int,
    on_progress: Optional[Callable[[dict], Awaitable[None]]] = None,
) -> list[GradedTimePeriod]:
    # Get each rubric category that exists in dynamo db
    results: list[GradedTimePeriod] = []
    to_grade: dict[RubricCategory, dict] = {}
    for category in RubricCategory:
        cfg = await asyncio.to_thread(get_rubric_directions, category)
        if cfg is None:
            continue
        # Check if already graded
        cached = await asyncio.to_thread(grade_store.load, tckr, start_year, end_year, category, cfg["version"])

        # If so add to results
        if cached is not None:
            results.append(cached)
        # Else add to the querey pipeline
        else:
            to_grade[category] = cfg

    if on_progress:
        await on_progress({"type": "categories", "total": len(to_grade), "cached": len(results)})
    if not to_grade:
        return results

    # For each cfg in to_grade.values() --> for each loc in cfg["locations"] --> add location to to set which becomes list
    union_locations = list({loc for cfg in to_grade.values() for loc in cfg["locations"]})
    blocks = await asyncio.to_thread(fetch_sections, tckr, start_year, end_year, union_locations)

    # 3. Pair each block with the to-grade categories that actually need it.
    def _categories_for(block: dict) -> list[RubricCategory]:
        section = section_from_form(block["form"], block["section"])
        # Get all categories that a given section belongs to
        return [c for c, cfg in to_grade.items() if section in cfg["locations"]]

    # Section, all categories that need that section
    block_categories = [(block, _categories_for(block)) for block in blocks]
    # Get total bedrock calls
    total_calls = sum(len(cats) for _, cats in block_categories)
    completed = 0
    # Dict of categories : list of tuples of (section_text(block), SectionMeta(result))
    metas: dict[RubricCategory, list[tuple[dict, SectionMeta]]] = {c: [] for c in to_grade}
    sem = asyncio.Semaphore(MAX_WORKERS)

    # Complete a section for a given category
    async def _run(block: dict, category: RubricCategory) -> None:
        nonlocal completed
        async with sem:
            meta = await asyncio.to_thread(extract_section_meta, tckr, block, category, to_grade[category])
        metas[category].append((block, meta))
        completed += 1
        if on_progress:
            await on_progress({
                "type": "progress",
                "completed": completed,
                "total": total_calls,
                "form": block["form"],
                "year": block["year"],
                "section": block["section"],
                "quarter": block.get("quarter"),
                "category": category.value,
            })

    # For each block(section_text) and category, if there are multiple categories sharing a section, 
    # Run and cache the first section sync, then the rest asyn off the cache
    for block, categories in block_categories:
        first, rest = categories[0], categories[1:]
        await _run(block, first)
        if rest:
            # Start unpacks list ito gather, does not take list
            await asyncio.gather(*[_run(block, category) for category in rest])

    # 5. Aggregate each to-grade category's collected findings into its final
    # grade, same as grade_section step 6.
    for category, cfg in to_grade.items():
        blocks_metas = metas[category]
        if not blocks_metas:
            results.append(no_evidence(category, start_year, end_year, "No cached filings found for this ticker/period."))
            continue
        labeled = [label_section_meta(block, meta) for block, meta in blocks_metas]
        graded = await asyncio.to_thread(aggregate_grade, tckr, category, cfg, labeled, start_year, end_year)
        results.append(graded)

    return results
