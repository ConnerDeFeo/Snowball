from utils.aws_clients import dynamo_client

TABLE_NAME = "snowball_section_grades"
client = dynamo_client()
table = client.Table(TABLE_NAME)

def get(tckr: str, category_period: str) -> dict | None:
    response = table.get_item(Key={"tckr": tckr, "category_period": category_period})
    return response.get("Item")

def put(tckr: str, category_period: str, **fields):
    table.put_item(Item={"tckr": tckr, "category_period": category_period, **fields})
