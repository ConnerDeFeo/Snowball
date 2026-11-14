from fastapi import APIRouter

from evidence.read_evidence import read_evidence
from evidence.run_checklist import run_checklist
from utils.sse import sse_response

router = APIRouter()


# Runs the checklist (all, one category, or one question) and streams progress.
@router.get("/evidence/run/{tckr}")
async def run_evidence_route(
    tckr: str, start_year: int, end_year: int,
    category_id: str | None = None, question_id: str | None = None,
):
    async def job(on_progress):
        result = await run_checklist(tckr, start_year, end_year, category_id, question_id, on_progress=on_progress)
        return {"type": "result", "categories": result}

    return sse_response(job)


# Reads stored evidence without calling the LLM.
@router.get("/evidence/{tckr}")
def get_evidence_route(
    tckr: str, start_year: int, end_year: int,
    category_id: str | None = None, question_id: str | None = None,
):
    return read_evidence(tckr, start_year, end_year, category_id, question_id)
