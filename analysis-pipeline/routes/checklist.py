from fastapi import APIRouter
from pydantic import BaseModel

from checklist import category, load, question, sub_agent

router = APIRouter()


class CategoryCreate(BaseModel):
    name: str
    order: int = 0


class CategoryEdit(BaseModel):
    name: str | None = None
    order: int | None = None


class QuestionCreate(BaseModel):
    text: str
    order: int = 0
    latest_only: bool = False


class QuestionEdit(BaseModel):
    text: str | None = None
    order: int | None = None
    latest_only: bool | None = None


class SubAgentCreate(BaseModel):
    form: str
    section: str
    prompt: str


class SubAgentEdit(BaseModel):
    form: str | None = None
    section: str | None = None
    prompt: str | None = None


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
    return {"id": question.create(category_id, req.text, req.order, req.latest_only)}


@router.patch("/checklist/{category_id}/questions/{qid}")
def edit_question(category_id: str, qid: str, req: QuestionEdit):
    question.edit(category_id, qid, req.text, req.order, req.latest_only)
    return {"status": "updated"}


@router.delete("/checklist/{category_id}/questions/{qid}")
def delete_question(category_id: str, qid: str):
    question.delete(category_id, qid)
    return {"status": "deleted"}


@router.post("/checklist/{category_id}/questions/{qid}/sub_agents")
def create_sub_agent(category_id: str, qid: str, req: SubAgentCreate):
    return {"id": sub_agent.create(category_id, qid, req.form, req.section, req.prompt)}


@router.patch("/checklist/{category_id}/questions/{qid}/sub_agents/{said}")
def edit_sub_agent(category_id: str, qid: str, said: str, req: SubAgentEdit):
    version = sub_agent.edit(category_id, qid, said, req.form, req.section, req.prompt)
    return {"version": version}


@router.delete("/checklist/{category_id}/questions/{qid}/sub_agents/{said}")
def delete_sub_agent(category_id: str, qid: str, said: str):
    sub_agent.delete(category_id, qid, said)
    return {"status": "deleted"}
