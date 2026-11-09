from botocore.exceptions import ClientError
from fastapi import HTTPException

from checklist.keys import META_SK, new_id, question_sk
from checklist.version import bump
from utils.dynamo import checklist_table


def create(category_id: str, text: str, order: int, latest_only: bool) -> str:
    if checklist_table.get(category_id, META_SK) is None:
        raise HTTPException(status_code=404, detail=f"category {category_id} not found")
    qid = new_id()
    checklist_table.create(category_id, question_sk(qid), text=text, order=order,
                           latest_only=latest_only, version="v1")
    return qid


def edit(category_id: str, qid: str, text: str | None, order: int | None, latest_only: bool | None) -> None:
    item = checklist_table.get(category_id, question_sk(qid))
    if item is None:
        raise HTTPException(status_code=404, detail=f"question {qid} not found")
    fields = {k: v for k, v in {"order": order, "latest_only": latest_only}.items() if v is not None}
    # Only the text feeds the sub-agent prompt, so only a text change
    # invalidates cached evidence. order/latest_only never touch the cache key.
    if text is not None and text != item["text"]:
        fields["text"] = text
        fields["version"] = bump(item["version"])
    if not fields:
        return
    try:
        checklist_table.update(category_id, question_sk(qid), **fields)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail=f"question {qid} not found")
        raise


# Deletes the question and all of its sub-agents.
def delete(category_id: str, qid: str) -> None:
    sk = question_sk(qid)
    for item in checklist_table.query_category(category_id):
        if item["sk"] == sk or item["sk"].startswith(f"{sk}#SA#"):
            checklist_table.delete(category_id, item["sk"])
