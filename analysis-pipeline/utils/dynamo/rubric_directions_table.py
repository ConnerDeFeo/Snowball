import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = "snowball_rubric_directions"
table = boto3.resource('dynamodb').Table(TABLE_NAME)

# Fetches every item (META + all location entries) for a rubric category in
# one round trip, since a grading run always needs the whole partition.
def query_category(rubric_category: str) -> list[dict]:
    response = table.query(KeyConditionExpression=Key("rubric_category").eq(rubric_category))
    return response.get("Items", [])
