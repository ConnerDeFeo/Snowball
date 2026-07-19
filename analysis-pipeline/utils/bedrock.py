import boto3

MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
client = boto3.client("bedrock-runtime")

def invoke(system: str, user: str) -> str:
    response = client.converse(
        modelId=MODEL_ID,
        system=[{"text": system}],
        messages=[{"role": "user", "content": [{"text": user}]}],
    )
    return response["output"]["message"]["content"][0]["text"]
