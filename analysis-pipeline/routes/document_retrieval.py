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
    start_date = body.get("start_date")
    end_date = body.get("end_date")
    if not start_date or not end_date:
        await send_error(websocket, "start_date and end_date are required")
        return

    # Range validation
    from_year, to_year = int(start_date[:4]), int(end_date[:4])
    if to_year < from_year or to_year - from_year >= MAX_YEARS:
        await send_error(websocket, f"date range may span at most {MAX_YEARS} years")
        return

    # Process documents
    try:
        found = await get_documents(tckr, start_date, end_date, on_progress=websocket.send_json)
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
