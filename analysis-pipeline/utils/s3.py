from utils.aws_clients import s3_client

BUCKET_NAME = "snowball-documents-bucket"
client = s3_client()

def store(key: str, body: bytes):
    client.put_object(Bucket=BUCKET_NAME, Key=key, Body=body)

def retrieve(key: str) -> bytes:
    response = client.get_object(Bucket=BUCKET_NAME, Key=key)
    return response["Body"].read()

def list_keys(prefix: str) -> list[str]:
    paginator = client.get_paginator("list_objects_v2")
    keys = []
    for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix):
        keys += [obj["Key"] for obj in page.get("Contents", [])]
    return keys
