from botocore.exceptions import ClientError
from fastapi import HTTPException

from checklist.keys import new_id, question_sk, sub_agent_sk
from checklist.version import bump
from enums.FormType import FormType
from enums.Sections import section_from_form
from utils.dynamo import checklist_table


# A target is one 10-K or 10-Q section; proxy statements aren't supported.
def _validate(form: str, section: str) -> None:
    if form not in (FormType.TEN_K.value, FormType.TEN_Q.value):
        raise HTTPException(status_code=400, detail=f"form must be {FormType.TEN_K.value} or {FormType.TEN_Q.value}")
    try:
        section_from_form(form, section)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"invalid form/section {form}#{section}: {e}")


def create(category_id: str, qid: str, form: str, section: str, prompt: str) -> str:
    _validate(form, section)
    if checklist_table.get(category_id, question_sk(qid)) is None:
        raise HTTPException(status_code=404, detail=f"question {qid} not found")
    said = new_id()
    checklist_table.create(category_id, sub_agent_sk(qid, said), form=form, section=section,
                           prompt=prompt, version="v1")
    return said


def edit(category_id: str, qid: str, said: str, form: str | None, section: str | None, prompt: str | None) -> str:
    sk = sub_agent_sk(qid, said)
    item = checklist_table.get(category_id, sk)
    if item is None:
        raise HTTPException(status_code=404, detail=f"sub-agent {said} not found")
    fields = {k: v for k, v in {"form": form, "section": section, "prompt": prompt}.items() if v is not None}
    _validate(fields.get("form", item["form"]), fields.get("section", item["section"]))
    # Any change to the target or prompt changes what the sub-agent produces.
    fields["version"] = bump(item["version"])
    try:
        checklist_table.update(category_id, sk, **fields)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail=f"sub-agent {said} not found")
        raise
    return fields["version"]


def delete(category_id: str, qid: str, said: str) -> None:
    checklist_table.delete(category_id, sub_agent_sk(qid, said))
