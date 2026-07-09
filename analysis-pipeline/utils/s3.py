import boto3
from dotenv import load_dotenv
import os

load_dotenv()
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
client = boto3.client('s3')

def store(self, key: str, body: bytes):
    client.put_object(Bucket=BUCKET_NAME, Key=key, Body=body)

def retrieve(self, key: str) -> bytes:
    response = self.client.get_object(Bucket=BUCKET_NAME, Key=key)
    return response["Body"].read()
