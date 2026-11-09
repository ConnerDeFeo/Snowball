from fastapi import APIRouter
from pydantic import BaseModel

from checklist import category, load, question

router = APIRouter()


class CategoryCreate(BaseModel):
    name: str
    order: int = 0


class CategoryEdit(BaseModel):
    name: str | None = None
    order: int | None = None


class QuestionCreate(BaseModel):
    text: str
    form: str
    section: str
    order: int = 0
    latest_only: bool = False


class QuestionEdit(BaseModel):
    text: str | None = None
    form: str | None = None
    section: str | None = None
    order: int | None = None
    latest_only: bool | None = None


@router.get("/checklist")
def get_all_categories():
    return load.get_all()


@router.post("/checklist")
def create_category(req: CategoryCreate):
    return {"id": category.create(req.name, req.order)}


@router.get("/checklist/{category_id}")
def get_category(category_id: str):
    return load.get_category(category_id)


@router.patch("/checklist/{category_id}")
def edit_category(category_id: str, req: CategoryEdit):
    category.edit(category_id, req.name, req.order)
    return {"status": "updated"}


@router.delete("/checklist/{category_id}")
def delete_category(category_id: str):
    category.delete(category_id)
    return {"status": "deleted"}


@router.post("/checklist/{category_id}/questions")
def create_question(category_id: str, req: QuestionCreate):
    return {"id": question.create(category_id, req.text, req.form, req.section, req.order, req.latest_only)}


@router.patch("/checklist/{category_id}/questions/{qid}")
def edit_question(category_id: str, qid: str, req: QuestionEdit):
    version = question.edit(category_id, qid, req.text, req.form, req.section, req.order, req.latest_only)
    return {"version": version}


@router.delete("/checklist/{category_id}/questions/{qid}")
def delete_question(category_id: str, qid: str):
    question.delete(category_id, qid)
    return {"status": "deleted"}
