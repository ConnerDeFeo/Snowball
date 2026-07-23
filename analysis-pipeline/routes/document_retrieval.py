import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from document_retrieval.get_documents import get_documents
from utils.websocket import receive_body, send_error

router = APIRouter()
logger = logging.getLogger(__name__)

MAX_YEARS = 6


@router.websocket("/documents/{tckr}")
async def documents(websocket: WebSocket, tckr: str):
    # Get ws
    body = await receive_body(websocket)
    if body is None:
        return

    # Get params
    start_year = body.get("start_year")
    end_year = body.get("end_year")
    if start_year is None or end_year is None:
        await send_error(websocket, "start_year and end_year are required")
        return
    start_year, end_year = int(start_year), int(end_year)

    # Range validation
    if end_year < start_year or end_year - start_year >= MAX_YEARS:
        await send_error(websocket, f"date range may span at most {MAX_YEARS} years")
        return

    # Process documents
    try:
        found = await get_documents(tckr, start_year, end_year, on_progress=websocket.send_json)
    except WebSocketDisconnect:
        return
    except Exception as e:
        logger.exception("[%s] document retrieval failed", tckr)
        await send_error(websocket, str(e))
        return

    if not found:
        await send_error(websocket, f"no company found for ticker: {tckr}")
        return

    # Close connection
    await websocket.send_json({"type": "done", "ticker": tckr})
    await websocket.close()
