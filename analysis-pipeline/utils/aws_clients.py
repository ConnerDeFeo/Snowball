# utils/aws_clients.py
import os
import boto3

_LOCAL_ENDPOINT = os.getenv("AWS_ENDPOINT_LOCAL_URL")

def dynamo_client():
    return boto3.resource("dynamodb", endpoint_url=_LOCAL_ENDPOINT)

def s3_client():
    return boto3.client("s3", endpoint_url=_LOCAL_ENDPOINT)

def bedrock_client():
    return boto3.client("bedrock-runtime")