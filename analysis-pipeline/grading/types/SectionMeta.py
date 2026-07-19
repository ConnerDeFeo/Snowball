from pydantic import BaseModel
from document_retrieval.FormType import FormType
from grading.enums.RubricCategory import RubricCategory
from grading.enums.Sections import Section

class Finding(BaseModel):
    feild: str
    value: str
    snippet: str
    status: str

class SectionMeta(BaseModel):
    # 10k / 10q / Proxy
    filing_type: FormType

    # Specific section this is looking at
    section: Section

    # which rubric category is this looking at
    rubric_category: RubricCategory

    # Findinfs based on what was given
    finding: list[Finding]

    # anything that the findings to not cover
    notable_anomalies: str
    
    # Was the section even there?
    section_present: bool