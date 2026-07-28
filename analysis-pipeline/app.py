# app.py
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from routes.document_retrieval import router as document_retrieval_router
from routes.grading import router as grading_router
from routes.health import router as health_router
from routes.rubric import router as rubric_router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

def create_app():
    app = FastAPI()

    app.include_router(document_retrieval_router)
    app.include_router(grading_router)
    app.include_router(health_router)
    app.include_router(rubric_router)

    # asyncio.to_thread's default executor is sized min(32, cpu_count + 4), which
    # on a small instance (e.g. 2 vCPUs) caps us at 6 — below grading's
    # MAX_WORKERS=8. These threads are all I/O-wait (Bedrock/S3/Dynamo), so a
    # bigger pool doesn't compete for CPU; it just removes an artificial ceiling.
    @app.on_event("startup")
    async def _size_thread_pool():
        asyncio.get_running_loop().set_default_executor(
            ThreadPoolExecutor(max_workers=32, thread_name_prefix="blocking")
        )

    return app

app = create_app()
