from utils.aws_clients import dynamo_client

TABLE_NAME = "snowball_companies"
client = dynamo_client()
table = client.Table(TABLE_NAME)

# Upserts the ticker's row so /companies can list it. Called on every grade
# write, so this is idempotent last-write-wins rather than conditional.
def upsert(tckr: str, start_year: int, end_year: int, last_graded_at: str) -> None:
    table.put_item(
        Item={
            "tckr": tckr,
            "start_year": start_year,
            "end_year": end_year,
            "last_graded_at": last_graded_at,
        }
    )

def scan_all() -> list[dict]:
    items = []
    kwargs = {}
    while True:
        response = table.scan(**kwargs)
        items.extend(response.get("Items", []))
        if "LastEvaluatedKey" not in response:
            return items
        kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
