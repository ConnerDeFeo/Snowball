from fastapi import APIRouter
from pydantic import BaseModel

from enums.RubricCategory import RubricCategory
from rubric import rubric_section, sub_agent

router = APIRouter()


class RubricCreateRequest(BaseModel):
    name: str
    directions: str


class RubricEditRequest(BaseModel):
    directions: str | None = None


class SubAgentRequest(BaseModel):
    form: str
    section: str
    prompt: str


@router.post("/rubric/{rubric_category}")
def create_rubric(rubric_category: RubricCategory, req: RubricCreateRequest):
    version = rubric_section.create(rubric_category, req.name, req.directions)
    return {"version": version}


@router.patch("/rubric/{rubric_category}")
def edit_rubric(rubric_category: RubricCategory, req: RubricEditRequest):
    version = rubric_section.edit(rubric_category, req.directions)
    return {"version": version}


@router.delete("/rubric/{rubric_category}")
def delete_rubric(rubric_category: RubricCategory):
    rubric_section.delete(rubric_category)
    return {"status": "deleted"}


@router.post("/rubric/{rubric_category}/sub_agent")
def create_sub_agent(rubric_category: RubricCategory, req: SubAgentRequest):
    version = sub_agent.create(rubric_category, req.form, req.section, req.prompt)
    return {"version": version}


@router.patch("/rubric/{rubric_category}/sub_agent")
def edit_sub_agent(rubric_category: RubricCategory, req: SubAgentRequest):
    version = sub_agent.edit(rubric_category, req.form, req.section, req.prompt)
    return {"version": version}


@router.delete("/rubric/{rubric_category}/sub_agent")
def delete_sub_agent(rubric_category: RubricCategory, form: str, section: str):
    sub_agent.delete(rubric_category, form, section)
    return {"status": "deleted"}
