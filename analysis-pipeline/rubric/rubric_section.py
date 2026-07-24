# Operations on a rubric category's META item — the row holding its name,
# summarizer directions, and the list of filing locations to read. ("Rubric
# section" here means this META row, as distinct from a filing section like
# TenKSection.PART_I_ITEM_1 — see enums/Sections.py.)
from botocore.exceptions import ClientError
from fastapi import HTTPException

from enums.RubricCategory import RubricCategory
from enums.Sections import section_from_location_key
from rubric.version import bump
from utils.dynamo import rubric_directions_table

META_SK = "META"


def _validate_locations(locations: list[str]) -> None:
    for location in locations:
        try:
            section_from_location_key(location)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"invalid location {location!r}: {e}")


def create(category: RubricCategory, name: str, directions: str, locations: list[str]) -> str:
    _validate_locations(locations)
    version = "v1"
    try:
        rubric_directions_table.create(
            category.value, META_SK,
            name=name, directions=directions, locations=locations, version=version,
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=409, detail=f"rubric {category.value} already exists")
        raise
    return version


def edit(category: RubricCategory, directions: str | None = None, locations: list[str] | None = None) -> str:
    if locations is not None:
        _validate_locations(locations)

    meta = rubric_directions_table.get(category.value, META_SK)
    if meta is None:
        raise HTTPException(status_code=404, detail=f"rubric {category.value} not found")

    fields = {}
    if directions is not None:
        fields["directions"] = directions
    if locations is not None:
        fields["locations"] = locations
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
    # Only the META row is removed — per-location sub-agent items are left in
    # place so re-adding a location later restores its prompt.
    rubric_directions_table.delete(category.value, META_SK)


# Shared with rubric/sub_agent.py: editing a sub-agent prompt also bumps META's
# version, since the grading cache key is keyed off META's version.
def bump_version(category: RubricCategory) -> str:
    meta = rubric_directions_table.get(category.value, META_SK)
    if meta is None:
        raise HTTPException(status_code=404, detail=f"rubric {category.value} not found")
    version = bump(meta["version"])
    rubric_directions_table.update(category.value, META_SK, version=version)
    return version
