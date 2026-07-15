import boto3

BUCKET_NAME = "snowball-documents-bucket"
client = boto3.client('s3')

def store(key: str, body: bytes):
    client.put_object(Bucket=BUCKET_NAME, Key=key, Body=body)

def retrieve(key: str) -> bytes:
    response = client.get_object(Bucket=BUCKET_NAME, Key=key)
    return response["Body"].read()
