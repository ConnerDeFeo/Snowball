# routes/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/grade_company/{tckr}")
def grade(tckr: str):
    return {"status": "ok"}
