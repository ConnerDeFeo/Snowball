# Operations on a formtype#section item — the row holding the prompt for the
# sub-agent that reads one filing section for a rubric category.
from botocore.exceptions import ClientError
from fastapi import HTTPException

from enums.RubricCategory import RubricCategory
from enums.Sections import section_from_form, section_location_key
from rubric import rubric_section
from rubric.version import bump
from utils.dynamo import rubric_directions_table


def _sk(form: str, section: str) -> str:
    try:
        parsed = section_from_form(form, section)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"invalid form/section {form}#{section}: {e}")
    return section_location_key(parsed)


def create(category: RubricCategory, form: str, section: str, prompt: str) -> str:
    sk = _sk(form, section)
    # This location becomes part of the category's grading scope (see
    # grading/rubric_directions.py), so bump META's version before writing the
    # row — 404s closed instead of widening scope on a write that then errors.
    rubric_section.bump_version(category)
    version = "v1"
    try:
        rubric_directions_table.create(category.value, sk, prompt=prompt, version=version)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=409, detail=f"direction {sk} already exists for {category.value}")
        raise
    return version


def edit(category: RubricCategory, form: str, section: str, prompt: str) -> str:
    sk = _sk(form, section)
    item = rubric_directions_table.get(category.value, sk)
    if item is None:
        raise HTTPException(status_code=404, detail=f"direction {sk} not found for {category.value}")

    version = bump(item["version"])
    try:
        rubric_directions_table.update(category.value, sk, prompt=prompt, version=version)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            raise HTTPException(status_code=404, detail=f"direction {sk} not found for {category.value}")
        raise

    # A sub-agent prompt edit invalidates cached findings for this direction,
    # but the aggregate grade is keyed off META's version, so bump that too.
    rubric_section.bump_version(category)
    return version


def delete(category: RubricCategory, form: str, section: str) -> None:
    sk = _sk(form, section)
    # Removing this location shrinks the category's grading scope, so bump
    # META first (see create, above). This also 404s if the category has no
    # META row, which delete previously never did.
    rubric_section.bump_version(category)
    rubric_directions_table.delete(category.value, sk)
