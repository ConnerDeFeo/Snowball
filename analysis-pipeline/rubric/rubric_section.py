# Operations on a rubric category's META item — the row holding its name and
# summarizer directions. ("Rubric section" here means this META row, as
# distinct from a filing section like TenKSection.PART_I_ITEM_1 — see
# enums/Sections.py.) Which filing locations to read is no longer stored here;
# it's derived from the category's sub-agent rows — see grading/rubric_directions.py.
from botocore.exceptions import ClientError
from fastapi import HTTPException

from enums.RubricCategory import RubricCategory
from rubric.version import bump
from utils.dynamo import rubric_directions_table

META_SK = "META"


# Shapes one category's partition (META + sub-agent rows) into a response body.
# Keyed by raw SK ("10-K#part_i_item_1") rather than parsed back into Section
# enums the way grading/rubric_directions.py does — the SK is already a plain
# JSON-safe string.
def _shape(category: str, items: list[dict]) -> dict | None:
    meta = next((i for i in items if i["sk"] == META_SK), None)
    if meta is None:
        return None
    return {
        "rubric_category": category,
        "name": meta["name"],
        "directions": meta["directions"],
        "version": meta["version"],
        "sub_agent_directions": {
            i["sk"]: {"prompt": i["prompt"], "version": i["version"]}
            for i in items if i["sk"] != META_SK
        },
    }


def get(category: RubricCategory) -> dict:
    shaped = _shape(category.value, rubric_directions_table.query_category(category.value))
    if shaped is None:
        raise HTTPException(status_code=404, detail=f"rubric {category.value} not found")
    return shaped


def get_all() -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for item in rubric_directions_table.scan_all():
        grouped.setdefault(item["rubric_category"], []).append(item)
    shaped = (_shape(cat, items) for cat, items in grouped.items())
    return sorted((s for s in shaped if s is not None), key=lambda s: s["rubric_category"])


def create(category: RubricCategory, name: str, directions: str) -> str:
    version = "v1"
    try:
        rubric_directions_table.create(
            category.value, META_SK,
            name=name, directions=directions, version=version,
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=409, detail=f"rubric {category.value} already exists")
        raise
    return version


def edit(category: RubricCategory, directions: str | None = None) -> str:
    meta = rubric_directions_table.get(category.value, META_SK)
    if meta is None:
        raise HTTPException(status_code=404, detail=f"rubric {category.value} not found")

    fields = {}
    if directions is not None:
        fields["directions"] = directions
    version = bump(meta["version"])
    fields["version"] = version

    try:
        rubric_directions_table.update(category.value, META_SK, **fields)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail=f"rubric {category.value} not found")
        raise
    return version


def delete(category: RubricCategory) -> None:
    # Clears the whole partition (META + every sub-agent row). Sub-agent SKs
    # now define the category's filing locations, so leaving them behind (as
    # this used to do) would let a re-created category silently inherit them.
    rubric_directions_table.delete_category(category.value)


# Shared with rubric/sub_agent.py: editing a sub-agent prompt also bumps META's
# version, since the grading cache key is keyed off META's version.
def bump_version(category: RubricCategory) -> str:
    meta = rubric_directions_table.get(category.value, META_SK)
    if meta is None:
        raise HTTPException(status_code=404, detail=f"rubric {category.value} not found")
    version = bump(meta["version"])
    rubric_directions_table.update(category.value, META_SK, version=version)
    return version
