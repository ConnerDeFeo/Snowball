import json
import os
import urllib.parse
import urllib.request

# Base URL of the analysis pipeline, e.g. http://analysis-pipeline:8000
BASE_URL = os.environ.get("ANALYSIS_PIPELINE_URL", "")

def _get(path: str, params: dict | None = None):
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.load(resp)

def get_checklist() -> list[dict]:
    return _get("/checklist")

def get_evidence(tckr: str, start_year: int, end_year: int, question_id: str) -> list[dict]:
    return _get(f"/evidence/{tckr}", {"start_year": start_year, "end_year": end_year, "question_id": question_id})
