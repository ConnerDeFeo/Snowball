from boto3.dynamodb.conditions import Key
from utils.aws_clients import dynamo_client
from utils.dynamo.split_key import split_key

TABLE_NAME = "snowball_section_grades"
client = dynamo_client()
table = client.Table(TABLE_NAME)

def get(tckr: str, category_period: str) -> dict | None:
    response = table.get_item(Key={"tckr": tckr, "category_period": category_period})
    return response.get("Item")

def put(tckr: str, category_period: str, **fields):
    table.put_item(Item={"tckr": tckr, "category_period": category_period, **fields})

# Paginates past DynamoDB's 1MB-per-response cap — grade items carry full
# reasoning/quotes text, so a single unpaginated call can silently truncate.
def query(tckr: str, category_period_prefix: str) -> list[dict]:
    items = []
    kwargs = {
        "KeyConditionExpression": Key("tckr").eq(tckr)
        & Key("category_period").begins_with(category_period_prefix)
    }
    while True:
        response = table.query(**kwargs)
        items.extend(response.get("Items", []))
        if "LastEvaluatedKey" not in response:
            return items
        kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]

# category_period is "{start}#{end}#{rubric_category}#{version}". Older rows
# written before the version segment was added only have 3 parts — treat
# those as version 0 so a versioned row always outranks a legacy one.
def version_sort_key(category_period: str) -> int:
    parts = split_key(category_period)
    if len(parts) < 4:
        return 0
    return int(parts[3].lstrip("v"))
