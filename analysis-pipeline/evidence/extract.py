from enums.Sections import Section, section_from_form
from evidence import evidence_cache
from evidence.instructions import SUB_AGENT_BASE_INSTRUCTIONS
from evidence.types import EvidenceResponse
from utils import llm
from utils.parse_response import invoke_parsed

# The prompt is split around a cache_control breakpoint: `cached_prefix` (section +
# excerpt) is identical for every question that reads this same block, so only
# the first one pays to process it; every other question's call reads it back
# from cache. `tail` (the question itself) is the part that varies.
#
# `use_cache` should only be True when another question will also read this
# same block — the cache write costs 1.25x normal input tokens, which is
# wasted if nothing ever reads it back.
def extract_evidence(section_text: str, section: Section, prompt: str, label: str = "", use_cache: bool = True) -> EvidenceResponse:
    cached_prefix = f"""
      Section: {section.value}

      Excerpt:
      {section_text}
    """
    tail = f"""
      Question: {prompt}
    """

    def _call() -> str:
        if use_cache:
            return llm.invoke_cached(SUB_AGENT_BASE_INSTRUCTIONS, cached_prefix, tail, label=label)
        return llm.invoke(SUB_AGENT_BASE_INSTRUCTIONS, cached_prefix + tail)

    return invoke_parsed(_call, EvidenceResponse, label=label)

# Runs one work item (question + block) through Claude and caches the result.
def extract_and_store(tckr: str, item: dict, use_cache: bool) -> EvidenceResponse:
    question, block = item["question"], item["block"]
    section = section_from_form(block["form"], block["section"])
    quarter = f"/{block['quarter']}" if "quarter" in block else ""
    label = f"block={tckr}/{block['form']}/{block['year']}{quarter}/{block['section']} question={question['id']}"
    evidence = extract_evidence(block["text"], section, question["text"], label=label, use_cache=use_cache)
    evidence_cache.store(tckr, question, block, evidence)
    return evidence
