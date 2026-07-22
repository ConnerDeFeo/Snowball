from grading.types.SectionMeta import Finding
from pydantic import BaseModel
from grading.enums.RubricCategory import RubricCategory
from grading.enums.Sections import *
from grading.constants.rubric_directions import (
    SUB_AGENT_BASE_INSTRUCTIONS,
    resolve_sub_agent_direction,
)
from utils import bedrock

class FindingsResponse(BaseModel):
    findings: list[Finding]
    notable_anomalies: str

# Extracts the given findings for the given section text
def extract_findings(section_text:str, rubric_category: RubricCategory, section:Section) -> FindingsResponse:
    direction = resolve_sub_agent_direction(rubric_category, section)

    user_prompt = f"""
      Category: {rubric_category.display}
      Section: {section.value}
      Directions: {direction["prompt"]}

      Excerpt:
      {section_text}
    """

    response = bedrock.invoke(SUB_AGENT_BASE_INSTRUCTIONS, user_prompt)
    return FindingsResponse.model_validate_json(response)
