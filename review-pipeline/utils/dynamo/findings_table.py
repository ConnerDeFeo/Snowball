import boto3
from boto3.dynamodb.conditions import Key
from split_key import split_key

TABLE_NAME = "snowball_findings"
table = boto3.resource('dynamodb').Table(TABLE_NAME)

def get(tckr: str, finding_key: str) -> dict | None:
    response = table.get_item(Key={"tckr": tckr, "finding_key": finding_key})
    return response.get("Item")

def put(tckr: str, finding_key: str, **fields):
    table.put_item(Item={"tckr": tckr, "finding_key": finding_key, **fields})

def query_prefix(tckr: str, finding_key_prefix: str) -> list[dict]:
    response = table.query(
        KeyConditionExpression=Key("tckr").eq(tckr)
        & Key("finding_key").begins_with(finding_key_prefix)
    )
    return response.get("Items", [])

def query_range(tckr: str, low: str, high: str) -> list[dict]:
    response = table.query(
        KeyConditionExpression=Key("tckr").eq(tckr)
        & Key("finding_key").between(low, high)
    )
    return response.get("Items", [])

# utils/finding_key.py
# Shared helpers for parsing snowball_findings sort keys:
#   year#form#period#rubric_category#section#version#model_id
# version is a compound "v{primary}-v{secondary}", e.g. "v1-v2".

def version_sort_key(finding_key: str) -> tuple[int, int, str]:
    parts = split_key(finding_key)
    version, model_id = parts[5], parts[6]
    primary, secondary = version.split("-")
    return (int(primary.lstrip("v")), int(secondary.lstrip("v")), model_id)
