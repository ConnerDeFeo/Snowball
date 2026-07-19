from typing import NamedTuple
from document_retrieval import FormType
from enums.RubricCategory import RubricCategory
from enums.TenKSection import TenKSection
from enums.TenQSection import TenQSection

class Finding(NamedTuple):
    feild: str
    value: str
    snippet: str
    status: str

class SectionMeta(NamedTuple):
    # accession num used for unique identification
    accession: str

    # 10k / 10q / Proxy
    filing_type: FormType

    # Specific section this is looking at
    section: TenKSection | TenQSection

    # which rubric category is this looking at
    rubric_category: RubricCategory

    # Findinfs based on what was given
    finding: list[Finding]

    # anything that the findings to not cover
    notable_anomalies: str
    
    # Was the section even there?
    section_present: bool