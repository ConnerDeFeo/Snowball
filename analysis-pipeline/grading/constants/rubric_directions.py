from enums.RubricCategory import RubricCategory
from enums.TenKSection import TenKSection
from enums.TenQSection import TenQSection

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

"""

SUB_AGENT_DIRECTIONS: dict[RubricCategory, dict[TenKSection | TenQSection, str]] = {

}