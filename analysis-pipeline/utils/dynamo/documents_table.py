from utils.aws_clients import dynamo_client

TABLE_NAME = "snowball_documents"
client = dynamo_client()
table = client.Table(TABLE_NAME)

def put(accession: str, **fields):
    table.put_item(Item={"accession": accession, **fields})

def get(accession: str) -> dict | None:
    response = table.get_item(Key={"accession": accession})
    return response.get("Item")
