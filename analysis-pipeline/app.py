# app.py
from fastapi import FastAPI
from routes.document_retrieval import router as document_retrieval_router
from routes.health import router as health_router

def create_app():
    app = FastAPI()

    app.include_router(document_retrieval_router)
    app.include_router(health_router)

    return app

app = create_app()
