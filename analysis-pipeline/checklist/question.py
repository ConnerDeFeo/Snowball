from botocore.exceptions import ClientError
from fastapi import HTTPException

from checklist.keys import META_SK, new_id, question_sk
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


def create(category_id: str, text: str, form: str, section: str, order: int, latest_only: bool) -> str:
    _validate(form, section)
    if checklist_table.get(category_id, META_SK) is None:
        raise HTTPException(status_code=404, detail=f"category {category_id} not found")
    qid = new_id()
    checklist_table.create(category_id, question_sk(qid), text=text, form=form, section=section,
                           order=order, latest_only=latest_only, version="v1")
    return qid


# Returns the question's version, bumped only if text/form/section changed
# (those change what the agent produces; order and latest_only don't).
def edit(category_id: str, qid: str, text: str | None, form: str | None, section: str | None,
         order: int | None, latest_only: bool | None) -> str:
    item = checklist_table.get(category_id, question_sk(qid))
    if item is None:
        raise HTTPException(status_code=404, detail=f"question {qid} not found")
    fields = {k: v for k, v in {"text": text, "form": form, "section": section,
                                "order": order, "latest_only": latest_only}.items() if v is not None}
    _validate(fields.get("form", item["form"]), fields.get("section", item["section"]))
    if any(k in fields for k in ("text", "form", "section")):
        fields["version"] = bump(item["version"])
    if not fields:
        return item["version"]
    try:
        checklist_table.update(category_id, question_sk(qid), **fields)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail=f"question {qid} not found")
        raise
    return fields.get("version", item["version"])


def delete(category_id: str, qid: str) -> None:
    checklist_table.delete(category_id, question_sk(qid))
