import boto3

TABLE_NAME = "snowball_findings"
table = boto3.resource('dynamodb').Table(TABLE_NAME)

def get(section_key: str, version_key: str) -> dict | None:
    response = table.get_item(Key={"section_key": section_key, "version_key": version_key})
    return response.get("Item")

def put(section_key: str, version_key: str, **fields):
    table.put_item(Item={"section_key": section_key, "version_key": version_key, **fields})
