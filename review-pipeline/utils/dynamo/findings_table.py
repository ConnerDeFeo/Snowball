import boto3
from boto3.dynamodb.conditions import Key

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
