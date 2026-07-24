import asyncio
from typing import Awaitable, Callable, Optional

from enums.RubricCategory import RubricCategory
from grading.rubric_directions import get_rubric_directions
from grading.extract_section import extract_section_meta, label_section_meta
from grading.aggregate_grade import aggregate_grade, no_evidence
from grading.fetch_sections import fetch_sections
from grading import grade_store
from grading.types.GradedTimePeriod import GradedTimePeriod

MAX_WORKERS = 8  # cap concurrent Bedrock sub-agent calls per grade_section run

async def grade_section(
    tckr: str,
    start_year: int,
    end_year: int,
    rubric_category: RubricCategory,
    # Callable function that takes dict param and returns awaitable nothing
    on_progress: Optional[Callable[[dict], Awaitable[None]]] = None,
) -> GradedTimePeriod:
    # 1. Look up where to look (section locations) and what to look for
    # (directions) for this rubric category.
    cfg = await asyncio.to_thread(get_rubric_directions, rubric_category)
    if cfg is None:
        return no_evidence(rubric_category, start_year, end_year, "No rubric directions defined yet for this category.")

    # If already graded, pull cached from dynamo
    cached = await asyncio.to_thread(grade_store.load, tckr, start_year, end_year, rubric_category, cfg["version"])
    if cached is not None:
        return cached

    # 3. Pull the cached filing text for those locations within the date window.
    blocks = await asyncio.to_thread(fetch_sections, tckr, start_year, end_year, cfg["locations"])
    if not blocks:
        return no_evidence(rubric_category, start_year, end_year, "No cached filings found for this ticker/period.")

    total = len(blocks)
    if on_progress:
        await on_progress({"type": "start", "total": total})

    # 4. Extract findings from each filing section in parallel — each call is
    # an independent, blocking Bedrock request, so threads overlap the I/O wait.
    # gather (not as_completed) keeps `metas` in `blocks` order for the zip below,
    # while each _run still reports progress as soon as its own block finishes.
    sem = asyncio.Semaphore(MAX_WORKERS)
    completed = 0

    async def _run(block: dict):
        nonlocal completed
        async with sem:
            meta = await asyncio.to_thread(extract_section_meta, tckr, block, rubric_category, cfg)
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

    # Turn data into actuall SetionMeta data structs
    labeled = [label_section_meta(block, meta) for block, meta in zip(blocks, metas)]

    # Finally call master agent to grade
    return await asyncio.to_thread(aggregate_grade, tckr, rubric_category, cfg, labeled, start_year, end_year)
