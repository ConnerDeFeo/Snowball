import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = "snowball_section_grades"
table = boto3.resource('dynamodb').Table(TABLE_NAME)

def get(tckr: str, category_period: str) -> dict | None:
    response = table.get_item(Key={"tckr": tckr, "category_period": category_period})
    return response.get("Item")

def put(tckr: str, category_period: str, **fields):
    table.put_item(Item={"tckr": tckr, "category_period": category_period, **fields})

def query(tckr: str, category_period_prefix: str) -> list[dict]:
    response = table.query(
        KeyConditionExpression=Key("tckr").eq(tckr)
        & Key("category_period").begins_with(category_period_prefix)
    )
    return response.get("Items", [])
