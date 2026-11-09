import asyncio
import logging
from datetime import datetime, timezone
from typing import Awaitable, Callable, Optional

from checklist import load
from evidence import assemble, evidence_cache, plan_work
from evidence.extract import extract_and_store
from evidence.fetch_sections import fetch_sections
from utils.dynamo import companies_table

logger = logging.getLogger(__name__)

MAX_WORKERS = 8  # cap concurrent Bedrock sub-agent calls per run

def _block_id(block: dict) -> tuple:
    return (block["form"], block["year"], block.get("quarter"), block["section"])

# Runs the selected part of the checklist (everything, one category, or one
# question) for one ticker/period. Fetches each unique filing section once, and
# runs the questions that share a section back-to-back so Bedrock prompt
# caching (see extract.extract_evidence) only pays to process that section's
# text once per block instead of once per question.
async def run_checklist(
    tckr: str,
    start_year: int,
    end_year: int,
    category_id: Optional[str] = None,
    question_id: Optional[str] = None,
    on_progress: Optional[Callable[[dict], Awaitable[None]]] = None,
) -> list[dict]:
    categories = await asyncio.to_thread(load.select, category_id, question_id)
    blocks = await asyncio.to_thread(fetch_sections, tckr, start_year, end_year, plan_work.locations(categories))
    work = plan_work.plan(categories, blocks)

    # Evidence cached under the current prompt + model versions needs no Bedrock call.
    cached = await asyncio.gather(*[
        asyncio.to_thread(evidence_cache.get_cached, tckr, w["question"], w["block"])
        for w in work
    ])
    done: list[tuple[dict, object]] = []
    pending: dict[tuple, list[dict]] = {}
    for item, evidence in zip(work, cached):
        if evidence is not None:
            done.append((item, evidence))
        else:
            pending.setdefault(_block_id(item["block"]), []).append(item)

    total = sum(len(items) for items in pending.values())
    if on_progress:
        await on_progress({"type": "start", "total": total, "cached": len(done)})

    sem = asyncio.Semaphore(MAX_WORKERS)
    completed = 0

    # A single question/block can fail (e.g. Bedrock returning unparseable
    # JSON after retries) without aborting the rest of the run — it's skipped,
    # so that question ends up with less evidence instead of no results at all.
    async def _run(item: dict, use_cache: bool) -> None:
        nonlocal completed
        block = item["block"]
        try:
            async with sem:
                evidence = await asyncio.to_thread(extract_and_store, tckr, item, use_cache)
        except Exception:
            logger.exception(
                "skipping question after extraction failure: tckr=%s form=%s year=%s section=%s question=%s",
                tckr, block["form"], block["year"], block["section"], item["question"]["id"],
            )
        else:
            done.append((item, evidence))
        completed += 1
        if on_progress:
            await on_progress({
                "type": "progress", "completed": completed, "total": total,
                "form": block["form"], "year": block["year"], "section": block["section"],
                "quarter": block.get("quarter"),
                "question_id": item["question"]["id"],
            })

    # use_cache is only True when a second question will actually read the
    # cachePoint back — a lone question paying the 1.25x cache-write premium
    # for a block nothing else reads is pure waste. Within a block, the first
    # question runs alone to write the cachePoint before the rest read off it.
    async def _run_block(items: list[dict]) -> None:
        use_cache = len(items) > 1
        await _run(items[0], use_cache)
        if items[1:]:
            await asyncio.gather(*[_run(item, use_cache) for item in items[1:]])

    await asyncio.gather(*[_run_block(items) for items in pending.values()])

    if done:
        now = datetime.now(timezone.utc).isoformat()
        await asyncio.to_thread(companies_table.upsert, tckr, start_year, end_year, now)

    entries = [
        assemble.entry(i["question"]["id"], i["block"]["form"], i["block"]["year"],
                       i["block"].get("quarter"), i["block"]["section"], ev)
        for i, ev in done
    ]
    return assemble.build(categories, entries)
