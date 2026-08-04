from grading.types.SectionMeta import Finding
from pydantic import BaseModel
from enums.RubricCategory import RubricCategory
from enums.Sections import *
from grading.rubric_directions import SUB_AGENT_BASE_INSTRUCTIONS
from grading.parse_response import invoke_parsed
from utils import bedrock

class FindingsResponse(BaseModel):
    findings: list[Finding]
    notable_anomalies: str

# Extracts the given findings for the given section text. `direction` is the
# already-resolved sub-agent direction for this rubric_category/section, so the
# caller and the findings cache always agree on which prompt/version was used.
#
# The prompt is split around a Bedrock cachePoint: `cached_prefix` (section +
# excerpt) is identical for every rubric category that reads this same block,
# so only the first category grading a given block pays to process it; every
# other category's call reads it back from cache. `tail` (category +
# directions) is the part that actually varies per category.
#
# `use_cache` should only be True when another category will also read this
# same block — the cachePoint write costs 1.25x normal input tokens, which is
# wasted if nothing ever reads it back.
def extract_findings(section_text: str, rubric_category: RubricCategory, section: Section, direction: dict, block_label: str = "", use_cache: bool = True) -> FindingsResponse:
    cached_prefix = f"""
      Section: {section.value}

      Excerpt:
      {section_text}
    """
    tail = f"""
      Category: {rubric_category.display}
      Directions: {direction["prompt"]}
    """

    label = f"block={block_label} category={rubric_category.value}"

    def _call() -> str:
        if use_cache:
            return bedrock.invoke_cached(SUB_AGENT_BASE_INSTRUCTIONS, cached_prefix, tail, label=label)
        return bedrock.invoke(SUB_AGENT_BASE_INSTRUCTIONS, cached_prefix + tail)

    return invoke_parsed(_call, FindingsResponse, label=label)
