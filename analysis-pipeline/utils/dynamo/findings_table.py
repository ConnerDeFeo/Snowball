from utils.aws_clients import dynamo_client

TABLE_NAME = "snowball_findings"
client = dynamo_client()
table = client.Table(TABLE_NAME)

def get(tckr: str, finding_key: str) -> dict | None:
    response = table.get_item(Key={"tckr": tckr, "finding_key": finding_key})
    return response.get("Item")

def put(tckr: str, finding_key: str, **fields):
    table.put_item(Item={"tckr": tckr, "finding_key": finding_key, **fields})
