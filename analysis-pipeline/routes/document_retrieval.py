import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from document_retrieval.get_documents import get_documents

router = APIRouter()
logger = logging.getLogger(__name__)

MAX_YEARS = 6


@router.websocket("/documents/{tckr}")
async def documents(websocket: WebSocket, tckr: str):
    await websocket.accept()

    # Get ws
    try:
        body = await websocket.receive_json()
    except WebSocketDisconnect:
        return

    # Get params
    from_date = body.get("from_date")
    to_date = body.get("to_date")
    if not from_date or not to_date:
        await websocket.send_json({"type": "error", "detail": "from_date and to_date are required"})
        await websocket.close()
        return

    # Range validation
    from_year, to_year = int(from_date[:4]), int(to_date[:4])
    if to_year < from_year or to_year - from_year >= MAX_YEARS:
        await websocket.send_json({"type": "error", "detail": f"date range may span at most {MAX_YEARS} years"})
        await websocket.close()
        return

    # Process documents
    try:
        found = await get_documents(tckr, from_date, to_date, on_progress=websocket.send_json)
    except WebSocketDisconnect:
        return
    except Exception as e:
        logger.exception("[%s] document retrieval failed", tckr)
        await websocket.send_json({"type": "error", "detail": str(e)})
        await websocket.close()
        return

    if not found:
        await websocket.send_json({"type": "error", "detail": f"no company found for ticker: {tckr}"})
        await websocket.close()
        return
    
    # Close connection
    await websocket.send_json({"type": "done", "ticker": tckr})
    await websocket.close()
