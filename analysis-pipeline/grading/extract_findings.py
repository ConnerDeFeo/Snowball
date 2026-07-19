from grading.types.SectionMeta import Finding
from pydantic import BaseModel
from enums.RubricCategory import RubricCategory
from enums.Sections import *

class FindingsResponse(BaseModel):
    findings: list[Finding]
    notable_anomalies: str

# Extracts the given findings for the given section text
# { "findings": list[Finding], "notable_anomalies": str }
def extract_findings(section_text:str, rubric_category: RubricCategory) -> FindingsResponse:
    return
