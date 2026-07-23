import asyncio
import json
import logging
from typing import Awaitable, Callable

from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)


def sse_frame(payload: dict) -> str:
    return f"data: {json.dumps(payload)}\n\n"


async def sse_stream(job: Callable[[Callable[[dict], Awaitable[None]]], Awaitable[dict]]):
    """Bridges a push-style on_progress callback to a pull-style async generator.

    `job` is awaited with an on_progress sink; its return value is streamed
    as the final event. Domain exceptions become an error frame instead of
    propagating, since the response has already started with a 200.
    """
    queue: asyncio.Queue = asyncio.Queue()

    async def run():
        try:
            # Start the job function handed down wiht on_progress for hte main function being a put into the queue
            # Outter queue.put returns the jobs final bit of information saying to wrap everything up
            await queue.put(await job(queue.put))
        except Exception as e:
            logger.exception("streaming job failed")
            await queue.put({"type": "error", "detail": str(e)})
        finally:
            await queue.put(None)

    task = asyncio.create_task(run())
    try:
        while (event := await queue.get()) is not None:
            yield sse_frame(event)
    finally:
        # Client disconnected mid-stream: cancel the domain task. Must stay
        # synchronous — this runs inside GeneratorExit/aclose(), where await
        # and yield are both disallowed.
        task.cancel()


def sse_response(job: Callable[[Callable[[dict], Awaitable[None]]], Awaitable[dict]]) -> StreamingResponse:
    return StreamingResponse(
        sse_stream(job),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    ) 
