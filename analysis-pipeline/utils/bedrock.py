import boto3

MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
client = boto3.client("bedrock-runtime")

def invoke(system: str, user: str) -> str:
    response = client.converse(
        modelId=MODEL_ID,
        system=[{"text": system}],
        messages=[{"role": "user", "content": [{"text": user}]}],
    )
    text = response["output"]["message"]["content"][0]["text"]
    return _strip_code_fence(text)

# Bedrock sometimes wraps JSON responses in a markdown code fence
# (```json ... ```) despite instructions not to. Strip it so callers can
# parse the response directly.
def _strip_code_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text[: -len("```")]
    return text.strip()
