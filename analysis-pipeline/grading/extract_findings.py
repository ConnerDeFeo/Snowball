from grading.types.SectionMeta import Finding
from pydantic import BaseModel
from enums.RubricCategory import RubricCategory
from enums.Sections import *
from grading.rubric_directions import SUB_AGENT_BASE_INSTRUCTIONS
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
def extract_findings(section_text: str, rubric_category: RubricCategory, section: Section, direction: dict) -> FindingsResponse:
    cached_prefix = f"""
      Section: {section.value}

      Excerpt:
      {section_text}
    """
    tail = f"""
      Category: {rubric_category.display}
      Directions: {direction["prompt"]}
    """

    response = bedrock.invoke_cached(SUB_AGENT_BASE_INSTRUCTIONS, cached_prefix, tail)
    return FindingsResponse.model_validate_json(response)
