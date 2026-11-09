from enums.Sections import Section, section_from_form
from evidence import evidence_cache
from evidence.instructions import SUB_AGENT_BASE_INSTRUCTIONS
from evidence.types import EvidenceResponse
from utils import bedrock
from utils.parse_response import invoke_parsed

# The prompt is split around a Bedrock cachePoint: `cached_prefix` (section +
# excerpt) is identical for every sub-agent that reads this same block, so only
# the first one pays to process it; every other sub-agent's call reads it back
# from cache. `tail` (question + directions) is the part that varies.
#
# `use_cache` should only be True when another sub-agent will also read this
# same block — the cachePoint write costs 1.25x normal input tokens, which is
# wasted if nothing ever reads it back.
def extract_evidence(section_text: str, section: Section, question_text: str, direction: str, label: str = "", use_cache: bool = True) -> EvidenceResponse:
    cached_prefix = f"""
      Section: {section.value}

      Excerpt:
      {section_text}
    """
    tail = f"""
      Question: {question_text}
      Directions: {direction}
    """

    def _call() -> str:
        if use_cache:
            return bedrock.invoke_cached(SUB_AGENT_BASE_INSTRUCTIONS, cached_prefix, tail, label=label)
        return bedrock.invoke(SUB_AGENT_BASE_INSTRUCTIONS, cached_prefix + tail)

    return invoke_parsed(_call, EvidenceResponse, label=label)

# Runs one work item (question + sub-agent + block) through Bedrock and caches
# the result.
def extract_and_store(tckr: str, item: dict, use_cache: bool) -> EvidenceResponse:
    question, sub_agent, block = item["question"], item["sub_agent"], item["block"]
    section = section_from_form(block["form"], block["section"])
    quarter = f"/{block['quarter']}" if "quarter" in block else ""
    label = f"block={tckr}/{block['form']}/{block['year']}{quarter}/{block['section']} question={question['id']} sub_agent={sub_agent['id']}"
    evidence = extract_evidence(block["text"], section, question["text"], sub_agent["prompt"], label=label, use_cache=use_cache)
    evidence_cache.store(tckr, question, sub_agent, block, evidence)
    return evidence
