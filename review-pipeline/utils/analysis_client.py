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

# Runs the analysis pipeline's document fetch (an SSE stream) to completion and returns
# its last frame: {"type": "done"} or {"type": "error", "detail": ...}. Progress frames
# arrive after each filing, so the timeout only trips if the stream stalls.
def fetch_documents(tckr: str, start_year: int, end_year: int) -> dict:
    query = urllib.parse.urlencode({"start_year": start_year, "end_year": end_year})
    last: dict = {"type": "error", "detail": "no response from document fetch"}
    with urllib.request.urlopen(f"{BASE_URL}/documents/{tckr}?{query}", timeout=300) as resp:
        for raw in resp:
            line = raw.decode("utf-8").strip()
            if line.startswith("data:"):
                last = json.loads(line[5:])
    return last
