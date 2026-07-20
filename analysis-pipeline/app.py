# app.py
from fastapi import FastAPI
from routes.document_retrieval import router as document_retrieval_router
from routes.grading import router as grading_router
from routes.health import router as health_router
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

    return app

app = create_app()
