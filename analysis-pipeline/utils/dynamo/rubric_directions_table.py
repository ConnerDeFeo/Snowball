import boto3
from boto3.dynamodb.conditions import Attr, Key

TABLE_NAME = "snowball_rubric_directions"
table = boto3.resource('dynamodb').Table(TABLE_NAME)

# Fetches every item (META + all location entries) for a rubric category in
# one round trip, since a grading run always needs the whole partition.
def query_category(rubric_category: str) -> list[dict]:
    response = table.query(KeyConditionExpression=Key("rubric_category").eq(rubric_category))
    return response.get("Items", [])

# Fetches every item across every rubric category in one round trip. The table
# is small (one partition per category), so a scan is cheaper than a query per
# category.
def scan_all() -> list[dict]:
    response = table.scan()
    return response.get("Items", [])

def get(rubric_category: str, sk: str) -> dict | None:
    response = table.get_item(Key={"rubric_category": rubric_category, "sk": sk})
    return response.get("Item")

# Creates a new item. Raises botocore.exceptions.ClientError
# (ConditionalCheckFailedException) if one already exists at this key, so a
# caller never silently clobbers an existing rubric/direction.
def create(rubric_category: str, sk: str, **fields) -> None:
    table.put_item(
        Item={"rubric_category": rubric_category, "sk": sk, **fields},
        ConditionExpression=Attr("sk").not_exists(),
    )

# Updates only the given fields on an existing item. Raises
# ConditionalCheckFailedException if the item doesn't exist yet.
def update(rubric_category: str, sk: str, **fields) -> None:
    names = {f"#{k}": k for k in fields}
    values = {f":{k}": v for k, v in fields.items()}
    expr = "SET " + ", ".join(f"#{k} = :{k}" for k in fields)
    table.update_item(
        Key={"rubric_category": rubric_category, "sk": sk},
        UpdateExpression=expr,
        ExpressionAttributeNames=names,
        ExpressionAttributeValues=values,
        ConditionExpression=Attr("sk").exists(),
    )

def delete(rubric_category: str, sk: str) -> None:
    table.delete_item(Key={"rubric_category": rubric_category, "sk": sk})

# Deletes every item in a category's partition (META + all sub-agent rows).
def delete_category(rubric_category: str) -> None:
    for item in query_category(rubric_category):
        delete(rubric_category, item["sk"])
