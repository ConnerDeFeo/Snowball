from fastapi import WebSocket, WebSocketDisconnect


async def receive_body(websocket: WebSocket) -> dict | None:
    await websocket.accept()
    try:
        return await websocket.receive_json()
    except WebSocketDisconnect:
        return None


async def send_error(websocket: WebSocket, detail: str) -> None:
    await websocket.send_json({"type": "error", "detail": detail})
    await websocket.close()
