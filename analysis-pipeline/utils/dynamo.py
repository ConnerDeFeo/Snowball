import boto3

TABLE_NAME = "snowball-documents"
table = boto3.resource('dynamodb').Table(TABLE_NAME)

def put(accession: str, **fields):
    table.put_item(Item={"accession": accession, **fields})

def get(accession: str) -> dict | None:
    response = table.get_item(Key={"accession": accession})
    return response.get("Item")
