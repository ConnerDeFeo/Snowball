from grading.enums.RubricCategory import RubricCategory
from grading.enums.Sections import *

BASE_INSTRUCTIONS = """
  You are grading one category of a company's free-cash-flow-predictive quality,
  based on excerpts from its SEC filings (10-K and 10-Q sections). You will be
  given the category name, directions for what to look for, and the relevant
  filing excerpts, each labeled with its form type, year, and section.

  Some excerpts may be missing (a filing wasn't cached, or the section was
  absent) — grade on whatever is available and note any material gaps in your
  reasoning instead of guessing.

  Respond with ONLY a JSON object, no other text, in this exact shape:
  {"grade": <integer 0-100>, "reasoning": "<string>", "quotes": ["<string>", ...]}

  - "grade": 0-100, where 0 is the weakest possible showing for this category
    and 100 is the strongest, based solely on the evidence in the excerpts.
  - "reasoning": a concise explanation of the grade, citing specific evidence.
  - "quotes": short verbatim quotes from the excerpts that support the grade.
"""

### THIS IS A STANDIN FOR NOW, FURTHER RESEARCH WILL BE DONE EXTENSIVLEY LATER ON ALL AREAS
### Proxy-only source material (exec bios, CD&A) is mapped to the closest 10-K item
### (Item 10 / Item 11), since the 10-K frequently incorporates it by reference and
### there's no dedicated proxy section enum yet.

RUBRIC_DIRECTIONS: dict[RubricCategory, dict] = {
    RubricCategory.REVENUE_DURABILITY : {
        "name": "Revenue durability",
        "locations": [
            TenKSection.PART_I_ITEM_1,      # Business - contract structure, recurring vs. project-based revenue, backlog
            TenKSection.PART_II_ITEM_7,     # MD&A - revenue drivers and disaggregation discussion
            TenKSection.PART_II_ITEM_8,     # Notes - Revenue Recognition footnote (ASC 606 disaggregation)
        ],
        "directions": "Determine what share of revenue is contractual, recurring, or subscription-based versus one-time or project-based, and how much visibility management has into future revenue (backlog, deferred revenue, remaining performance obligations).",
    },
    RubricCategory.REVENUE_QUALITY : {
        "name": "Revenue quality",
        "locations": [
            TenKSection.PART_II_ITEM_7,     # MD&A - discussion of one-time items, divestiture gains, or channel stuffing risk
            TenKSection.PART_II_ITEM_8,     # Notes - Revenue Recognition footnote (timing of recognition, contract assets/liabilities)
            TenQSection.PART_I_ITEM_1,      # Financial Statements - quarter-over-quarter revenue trend and any restatements
            TenQSection.PART_I_ITEM_2,      # MD&A - quarterly commentary on revenue trend
        ],
        "directions": "Assess whether reported revenue reflects real cash-backed demand versus aggressive recognition timing, non-recurring gains, or channel-stuffing, using the recognition footnote and any MD&A caveats.",
    }
}

SUB_AGENT_BASE_INSTRUCTIONS = """
  You are extracting findings from a single excerpt of a company's SEC filing
  (one section, one form) that are relevant to one grading category. You will be
  given the category name, directions for what to look for in this section, and
  the excerpt text.

  Pull out discrete, factual findings only — do not grade or score anything.
  If the excerpt doesn't contain anything relevant to the directions, return an
  empty findings list rather than guessing.

  Respond with ONLY a JSON object, no other text, in this exact shape:
  {"findings": [{"field": "<string>", "value": "<string>", "snippet": "<string>", "status": "<string>"}, ...],
   "notable_anomalies": "<string>"}

  - "field": short name of what this finding is about (e.g. "backlog", "deferred revenue").
  - "value": the extracted fact or figure, in a few words.
  - "snippet": a short verbatim quote from the excerpt supporting this finding.
  - "status": one of "discolsed" or "not_disclosed" explaining if the relavent information is even there
    this finding was pulled from the excerpt.
  - "notable_anomalies": anything odd or noteworthy in the excerpt that the
    findings above don't capture, or an empty string if nothing stands out.
"""

### PLACEHOLDER — scaffolding only, real per-section directions to be researched later
SUB_AGENT_DIRECTIONS: dict[RubricCategory, dict[TenKSection | TenQSection, str]] = {
    RubricCategory.REVENUE_DURABILITY: {
        TenKSection.PART_I_ITEM_1: "Look for contract structure, recurring vs. project-based revenue, and backlog figures.",
        TenKSection.PART_II_ITEM_7: "Look for management's discussion of revenue drivers and disaggregation.",
        TenKSection.PART_II_ITEM_8: "Look for the Revenue Recognition footnote, including ASC 606 disaggregation and remaining performance obligations.",
    },
    RubricCategory.REVENUE_QUALITY: {
        TenKSection.PART_II_ITEM_7: "Look for discussion of one-time items, divestiture gains, or channel-stuffing risk.",
        TenKSection.PART_II_ITEM_8: "Look for the Revenue Recognition footnote's detail on timing of recognition and contract assets/liabilities.",
        TenQSection.PART_I_ITEM_1: "Look for quarter-over-quarter revenue trend and any restatements in the financial statements.",
        TenQSection.PART_I_ITEM_2: "Look for quarterly MD&A commentary on revenue trend.",
    },
}

### Fallback directions used when a category/section pair has no specific entry above
DEFAULT_SUB_AGENT_DIRECTIONS = "Extract any findings in this excerpt relevant to this grading category."