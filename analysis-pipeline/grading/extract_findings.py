from grading.types.SectionMeta import Finding
from pydantic import BaseModel
from grading.enums.RubricCategory import RubricCategory
from grading.enums.Sections import *
from grading.constants.rubric_directions import (
    SUB_AGENT_BASE_INSTRUCTIONS,
    SUB_AGENT_DIRECTIONS,
    DEFAULT_SUB_AGENT_DIRECTIONS,
)
from utils import bedrock

class FindingsResponse(BaseModel):
    findings: list[Finding]
    notable_anomalies: str

# Extracts the given findings for the given section text
def extract_findings(section_text:str, rubric_category: RubricCategory, section:Section) -> FindingsResponse:
    directions = SUB_AGENT_DIRECTIONS.get(rubric_category, {}).get(section, DEFAULT_SUB_AGENT_DIRECTIONS)

    user_prompt = f"""
      Category: {rubric_category.value}
      Section: {section.value}
      Directions: {directions}

      Excerpt:
      {section_text}
    """

    response = bedrock.invoke(SUB_AGENT_BASE_INSTRUCTIONS, user_prompt)
    return FindingsResponse.model_validate_json(response)
