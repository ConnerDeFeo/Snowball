import logging

from grading.types.SectionMeta import Finding
from pydantic import BaseModel, ValidationError
from enums.RubricCategory import RubricCategory
from enums.Sections import *
from grading.rubric_directions import SUB_AGENT_BASE_INSTRUCTIONS
from utils import bedrock

logger = logging.getLogger(__name__)

MAX_PARSE_ATTEMPTS = 3  # 1 initial try + 2 retries on invalid JSON

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

    # Bedrock occasionally emits structurally invalid JSON (e.g. an unescaped
    # quote inside a verbatim filing "snippet"), even with stop_reason=end_turn.
    # Retry a few times before giving up, since re-sampling usually produces
    # valid JSON.
    last_error: ValidationError | None = None
    for attempt in range(1, MAX_PARSE_ATTEMPTS + 1):
        if use_cache:
            response = bedrock.invoke_cached(SUB_AGENT_BASE_INSTRUCTIONS, cached_prefix, tail, label=label)
        else:
            response = bedrock.invoke(SUB_AGENT_BASE_INSTRUCTIONS, cached_prefix + tail)
        try:
            return FindingsResponse.model_validate_json(response)
        except ValidationError as e:
            last_error = e
            logger.warning("invalid findings JSON: %s attempt=%d/%d", label, attempt, MAX_PARSE_ATTEMPTS)

    raise last_error
