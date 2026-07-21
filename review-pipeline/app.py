# app.py
from fastapi import FastAPI
from routes.health import router as health_router
from routes.review import router as review_router

def create_app():
    app = FastAPI()

    app.include_router(health_router)
    app.include_router(review_router)

    return app

app = create_app()
