# utils/aws_clients.py
import boto3


def dynamo_client():
    return boto3.resource("dynamodb")

def s3_client():
    return boto3.client("s3")