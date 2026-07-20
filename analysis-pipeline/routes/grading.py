# routes/grading.py
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from grading.enums.RubricCategory import RubricCategory
from grading.grade_section import grade_section

router = APIRouter()
logger = logging.getLogger(__name__)

class GradeRequest(BaseModel):
    start_year: int
    end_year: int

@router.post("/grade_company/{tckr}")
def grade(tckr: str, grade_request: GradeRequest):
    return {"status": "ok"}

@router.websocket("/grade_section/{tckr}")
async def grade_section_route(websocket: WebSocket, tckr: str):
    await websocket.accept()

    # Get params
    try:
        body = await websocket.receive_json()
    except WebSocketDisconnect:
        return

    start_date = body.get("start_date")
    end_date = body.get("end_date")
    if not start_date or not end_date or not body.get("rubric_category"):
        await websocket.send_json({"type": "error", "detail": "start_date, end_date, and rubric_category are required"})
        await websocket.close()
        return

    # RubricCategory doesn't auto-coerce from raw JSON like a Pydantic body would
    try:
        rubric_category = RubricCategory(body["rubric_category"])
    except ValueError:
        await websocket.send_json({"type": "error", "detail": f"invalid rubric_category: {body['rubric_category']}"})
        await websocket.close()
        return

    # Grade section, streaming sub-agent progress as they wrap up
    try:
        graded = await grade_section(tckr, start_date, end_date, rubric_category, on_progress=websocket.send_json)
    except WebSocketDisconnect:
        return
    except Exception as e:
        logger.exception("[%s] grading failed", tckr)
        await websocket.send_json({"type": "error", "detail": str(e)})
        await websocket.close()
        return

    # Final message: the graded section from the master agent
    await websocket.send_json({"type": "result", "graded": graded.model_dump(mode="json")})
    await websocket.close()
