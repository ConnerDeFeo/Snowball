import logging
import time

import boto3

MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
client = boto3.client("bedrock-runtime")
logger = logging.getLogger(__name__)

# Shared converse call + logging, driven off already-built content blocks so
# callers can either send one plain text block (invoke) or a cached-prefix +
# cachePoint + tail split (invoke_cached) without duplicating the request/
# logging plumbing.
def _converse(system: str, content: list[dict]) -> str:
    start = time.perf_counter()
    response = client.converse(
        modelId=MODEL_ID,
        system=[{"text": system}],
        messages=[{"role": "user", "content": content}],
    )
    elapsed = time.perf_counter() - start
    usage = response["usage"]
    logger.info(
        "bedrock invoke: model=%s input_tokens=%d output_tokens=%d total_tokens=%d "
        "cache_read_tokens=%s cache_write_tokens=%s stop_reason=%s "
        "latency_ms=%s elapsed=%.2fs request_id=%s",
        MODEL_ID,
        usage["inputTokens"],
        usage["outputTokens"],
        usage.get("totalTokens"),
        usage.get("cacheReadInputTokens"),
        usage.get("cacheWriteInputTokens"),
        response.get("stopReason"),
        response.get("metrics", {}).get("latencyMs"),
        elapsed,
        response.get("ResponseMetadata", {}).get("RequestId"),
    )
    text = response["output"]["message"]["content"][0]["text"]
    return _strip_code_fence(text)

def invoke(system: str, user: str) -> str:
    return _converse(system, [{"text": user}])

# Same call, but splits the prompt into a cached prefix and a variable tail
# around a cachePoint. Callers must keep `cached_prefix` byte-identical across
# invocations that should share the cache (e.g. the same filing excerpt read
# by multiple rubric categories).
def invoke_cached(system: str, cached_prefix: str, tail: str) -> str:
    content = [
        {"text": cached_prefix},
        {"cachePoint": {"type": "default"}},
        {"text": tail},
    ]
    return _converse(system, content)

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
