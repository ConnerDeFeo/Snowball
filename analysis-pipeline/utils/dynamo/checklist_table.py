from boto3.dynamodb.conditions import Attr, Key
from utils.aws_clients import dynamo_client

TABLE_NAME = "snowball_checklist"
client = dynamo_client()
table = client.Table(TABLE_NAME)

# Every item (META + questions + sub-agents) in a category's partition, in one
# round trip, since a run or a GET always needs the whole partition.
def query_category(category_id: str) -> list[dict]:
    response = table.query(KeyConditionExpression=Key("category_id").eq(category_id))
    return response.get("Items", [])

# Every item across every category. The table is small (one partition per
# category), so a scan is cheaper than a query per category.
def scan_all() -> list[dict]:
    response = table.scan()
    return response.get("Items", [])

def get(category_id: str, sk: str) -> dict | None:
    response = table.get_item(Key={"category_id": category_id, "sk": sk})
    return response.get("Item")

# Raises ClientError (ConditionalCheckFailedException) if the key already
# exists, so a caller never silently clobbers an existing item.
def create(category_id: str, sk: str, **fields) -> None:
    table.put_item(
        Item={"category_id": category_id, "sk": sk, **fields},
        ConditionExpression=Attr("sk").not_exists(),
    )

# Updates only the given fields. Raises ConditionalCheckFailedException if the
# item doesn't exist.
def update(category_id: str, sk: str, **fields) -> None:
    names = {f"#{k}": k for k in fields}
    values = {f":{k}": v for k, v in fields.items()}
    expr = "SET " + ", ".join(f"#{k} = :{k}" for k in fields)
    table.update_item(
        Key={"category_id": category_id, "sk": sk},
        UpdateExpression=expr,
        ExpressionAttributeNames=names,
        ExpressionAttributeValues=values,
        ConditionExpression=Attr("sk").exists(),
    )

def delete(category_id: str, sk: str) -> None:
    table.delete_item(Key={"category_id": category_id, "sk": sk})
