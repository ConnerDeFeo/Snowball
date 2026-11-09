### Bumping this invalidates every cached piece of evidence, since the stored
### version combines this with each sub-agent's own version.
BASE_VERSION = "v4"

SUB_AGENT_BASE_INSTRUCTIONS = """
  You are extracting evidence from a single excerpt of a company's SEC filing
  (one section, one form). You will be given a question and the excerpt text,
  and should pull out what is relevant to that question.

  Pull out discrete, factual findings only — do not grade, score, or summarize
  anything. If the excerpt doesn't contain anything relevant to the question,
  return an empty findings list rather than guessing.

  Respond with ONLY a JSON object, no other text, in this exact shape:
  {"findings": [{"field": "<string>", "value": "<string>", "snippet": "<string>", "status": "<string>"}, ...]}

  - "field": short name of what this finding is about (e.g. "backlog", "deferred revenue").
  - "value": the extracted fact or figure, in a few words.
  - "snippet": a short verbatim quote from the excerpt supporting this finding.
  - "status": one of "disclosed" or "not_disclosed" explaining if the relevant information is even there
    this finding was pulled from the excerpt."""
