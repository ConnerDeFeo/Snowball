# tools/tool_log.py
# Compact per-turn record of tool calls, saved into session history so the agent
# remembers what it already read without storing the full (huge) tool results.
DIGEST_CHARS = 200


def record_call(log: list[dict], call: dict) -> None:
    log.append({"id": call.get("id"), "name": call["name"], "args": call.get("args", {}), "digest": ""})


def record_result(log: list[dict], tool_msg) -> None:
    text = tool_msg.content if isinstance(tool_msg.content, str) else str(tool_msg.content)
    snippet = " ".join(text.split())[:DIGEST_CHARS]
    digest = f'{len(text):,} chars: "{snippet}"'
    for entry in log:
        if entry["id"] == getattr(tool_msg, "tool_call_id", None):
            entry["digest"] = digest
            return


def format_log(log: list[dict]) -> str:
    lines, seen = [], set()
    for e in log:
        args = ", ".join(f"{k}={v}" for k, v in e["args"].items())
        line = f"- {e['name']}({args}) -> {e['digest']}"
        if line not in seen:
            seen.add(line)
            lines.append(line)
    return "\n".join(lines)
