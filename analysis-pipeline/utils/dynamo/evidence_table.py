from boto3.dynamodb.conditions import Key
from utils.aws_clients import dynamo_client

TABLE_NAME = "snowball_evidence"
client = dynamo_client()
table = client.Table(TABLE_NAME)

def get(tckr: str, evidence_key: str) -> dict | None:
    response = table.get_item(Key={"tckr": tckr, "evidence_key": evidence_key})
    return response.get("Item")

def put(tckr: str, evidence_key: str, **fields):
    table.put_item(Item={"tckr": tckr, "evidence_key": evidence_key, **fields})

# Paginates past DynamoDB's 1MB-per-response cap — evidence items carry
# verbatim snippets, so a single unpaginated call can silently truncate.
def query_prefix(tckr: str, prefix: str) -> list[dict]:
    items = []
    kwargs = {
        "KeyConditionExpression": Key("tckr").eq(tckr) & Key("evidence_key").begins_with(prefix)
    }
    while True:
        response = table.query(**kwargs)
        items.extend(response.get("Items", []))
        if "LastEvaluatedKey" not in response:
            return items
        kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
