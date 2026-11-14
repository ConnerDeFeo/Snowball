import logging
import time

import anthropic

MODEL_ID = "claude-haiku-5-5"
MAX_TOKENS = 16000
# Auth comes from the mounted Anthropic profile (ANTHROPIC_CONFIG_DIR), no API key.
client = anthropic.Anthropic()
logger = logging.getLogger(__name__)

# Shared messages call + logging, driven off already-built content blocks so
# callers can either send one plain text block (invoke) or a cached-prefix +
# tail split (invoke_cached) without duplicating the request/logging plumbing.
def _create(system: str, content: list[dict], label: str = "") -> str:
    start = time.perf_counter()
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": content}],
        output_config={"effort": "low"},
    )
    elapsed = time.perf_counter() - start
    usage = response.usage
    cache_read = usage.cache_read_input_tokens
    cache_write = usage.cache_creation_input_tokens
    logger.info(
        "llm invoke: %s model=%s input_tokens=%d output_tokens=%d "
        "cache_read_tokens=%s cache_write_tokens=%s stop_reason=%s "
        "elapsed=%.2fs request_id=%s",
        label,
        MODEL_ID,
        usage.input_tokens,
        usage.output_tokens,
        cache_read,
        cache_write,
        response.stop_reason,
        elapsed,
        response.id,
    )
    # cache_write>0 means this block was just written to cache (first question
    # to read it), cache_read>0 means it was served from cache (a later
    # question reusing the same block).
    if cache_read:
        logger.info("llm cache HIT: %s cache_read_tokens=%d", label, cache_read)
    if cache_write:
        logger.info("llm cache WRITE: %s cache_write_tokens=%d", label, cache_write)
    # Thinking blocks may precede the answer; keep only the text blocks.
    text = "".join(b.text for b in response.content if b.type == "text")
    return _strip_code_fence(text)

def invoke(system: str, user: str) -> str:
    return _create(system, [{"type": "text", "text": user}])

# Same call, but splits the prompt into a cached prefix and a variable tail
# with a cache_control breakpoint on the prefix. Callers must keep
# `cached_prefix` byte-identical across invocations that should share the cache
# (e.g. the same filing excerpt read by multiple questions). `label` identifies
# the block/question for the cache HIT/WRITE log lines, so caching can be
# observed per block.
def invoke_cached(system: str, cached_prefix: str, tail: str, label: str = "") -> str:
    content = [
        {"type": "text", "text": cached_prefix, "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": tail},
    ]
    return _create(system, content, label=label)

# Claude sometimes wraps JSON responses in a markdown code fence
# (```json ... ```) despite instructions not to. Strip it so callers can
# parse the response directly.
def _strip_code_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text[: -len("```")]
    return text.strip()
