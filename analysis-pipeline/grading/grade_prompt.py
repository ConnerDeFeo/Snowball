import json

import boto3

from grading.constants.rubric_directions import BASE_INSTRUCTIONS

BEDROCK_REGION = "us-east-2"
HAIKU_MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

bedrock_client = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)


def build_prompt(category_meta: dict, sections: list[dict]) -> str:
    if sections:
        excerpts = "\n\n".join(
            f"=== {block['form']} {block['year']}"
            f"{' ' + block['quarter'] if 'quarter' in block else ''} · {block['section']} ===\n"
            f"{block['text']}"
            for block in sections
        )
    else:
        excerpts = "(no filing excerpts were available for this category/time period)"

    return (
        f"{BASE_INSTRUCTIONS}\n"
        f"Category: {category_meta['name']}\n"
        f"Directions: {category_meta['directions']}\n\n"
        f"Filing excerpts:\n{excerpts}"
    )


def invoke_bedrock(prompt: str) -> dict:
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}],
    })
    response = bedrock_client.invoke_model(modelId=HAIKU_MODEL_ID, body=body)
    payload = json.loads(response["body"].read())
    text = payload["content"][0]["text"]
    return json.loads(text)
