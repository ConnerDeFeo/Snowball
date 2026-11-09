from botocore.exceptions import ClientError
from fastapi import HTTPException

from checklist.keys import META_SK, new_id
from utils.dynamo import checklist_table


def create(name: str, order: int) -> str:
    category_id = new_id()
    checklist_table.create(category_id, META_SK, name=name, order=order)
    return category_id


def edit(category_id: str, name: str | None, order: int | None) -> None:
    fields = {k: v for k, v in {"name": name, "order": order}.items() if v is not None}
    if not fields:
        return
    try:
        checklist_table.update(category_id, META_SK, **fields)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail=f"category {category_id} not found")
        raise


# Clears the whole partition (META + every question).
def delete(category_id: str) -> None:
    for item in checklist_table.query_category(category_id):
        checklist_table.delete(category_id, item["sk"])
