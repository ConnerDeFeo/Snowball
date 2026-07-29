import time

from utils.aws_clients import dynamo_client

TABLE_NAME = "snowball_review_sessions"
MAX_HISTORY_MESSAGES = 20  # 10 turns, bounds prompt growth
TTL_SECONDS = 30 * 24 * 60 * 60  # 30 days, refreshed on every write

client = dynamo_client()
table = client.Table(TABLE_NAME)

# Unknown/expired session_id returns empty history rather than erroring, so
# the caller can transparently start a fresh conversation under that id.
def get_history(session_id: str) -> list[dict]:
    response = table.get_item(Key={"session_id": session_id})
    item = response.get("Item")
    return item["messages"] if item else []

def save_history(session_id: str, messages: list[dict]) -> None:
    table.put_item(
        Item={
            "session_id": session_id,
            "messages": messages[-MAX_HISTORY_MESSAGES:],
            "expires_at": int(time.time()) + TTL_SECONDS,
        }
    )
