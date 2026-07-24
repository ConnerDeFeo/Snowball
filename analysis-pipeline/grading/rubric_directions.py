from grading.enums.RubricCategory import RubricCategory
from grading.enums.Sections import Section, section_from_location_key
from utils.dynamo import rubric_directions_table

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

### Bumping this invalidates the cached findings for every direction below, since
### the stored prompt version combines this with each direction's own version.
SUB_AGENT_BASE_VERSION = "v1"

### Fallback direction used when a category/section pair has no specific entry
### in the rubric_directions table.
DEFAULT_SUB_AGENT_DIRECTIONS = {
    "prompt": "Extract any findings in this excerpt relevant to this grading category.",
    "version": "v1",
}

# Loads a rubric category's META item (name/directions/locations) plus every
# per-section sub-agent direction from the snowball_rubric_directions table,
# and shapes them into the dict grade_section/etc consume. Queried fresh every
# call (no process-level caching) so an operator's prompt edit is picked up on
# the very next grading run, without a redeploy.
#
# Returns None if the category has no META item yet (mirrors the old
# RUBRIC_DIRECTIONS.get(...) is None behavior).
def get_rubric_directions(rubric_category: RubricCategory) -> dict | None:
    items = rubric_directions_table.query_category(rubric_category.value)
    meta = next((item for item in items if item["sk"] == "META"), None)
    if meta is None:
        return None

    sub_agent_directions = {item["sk"]: item for item in items if item["sk"] != "META"}
    return {
        "name": meta["name"],
        "directions": meta["directions"],
        "locations": [section_from_location_key(key) for key in meta["locations"]],
        "sub_agent_directions": sub_agent_directions,
    }

# Looks up the sub-agent direction for a form/section within an already-loaded
# rubric config, falling back to the default when no specific entry exists.
# Single source of truth so extract_findings and the findings cache key always
# agree on which direction was used.
def resolve_sub_agent_direction(config: dict, form: str, section: Section) -> dict:
    key = f"{form}#{section.value}"
    return config["sub_agent_directions"].get(key, DEFAULT_SUB_AGENT_DIRECTIONS)

# Combines the shared base-instructions version with a direction's own version,
# so bumping either one invalidates cached findings that used the old prompt.
def sub_agent_prompt_version(direction: dict) -> str:
    return f"{SUB_AGENT_BASE_VERSION}-{direction['version']}"
