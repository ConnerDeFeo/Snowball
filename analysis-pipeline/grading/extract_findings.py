from grading.types.SectionMeta import Finding
from pydantic import BaseModel
from grading.enums.RubricCategory import RubricCategory
from grading.enums.Sections import *
from grading.rubric_directions import SUB_AGENT_BASE_INSTRUCTIONS
from utils import bedrock

class FindingsResponse(BaseModel):
    findings: list[Finding]
    notable_anomalies: str

# Extracts the given findings for the given section text. `direction` is the
# already-resolved sub-agent direction for this rubric_category/section, so the
# caller and the findings cache always agree on which prompt/version was used.
def extract_findings(section_text: str, rubric_category: RubricCategory, section: Section, direction: dict) -> FindingsResponse:
    user_prompt = f"""
      Category: {rubric_category.display}
      Section: {section.value}
      Directions: {direction["prompt"]}

      Excerpt:
      {section_text}
    """

    response = bedrock.invoke(SUB_AGENT_BASE_INSTRUCTIONS, user_prompt)
    return FindingsResponse.model_validate_json(response)
