import logging
from typing import Callable, TypeVar

from pydantic import BaseModel, ValidationError

logger = logging.getLogger(__name__)

MAX_PARSE_ATTEMPTS = 3  # 1 initial try + 2 retries on invalid JSON

T = TypeVar("T", bound=BaseModel)

# Bedrock occasionally emits structurally invalid JSON (e.g. an unescaped
# quote inside a verbatim filing quote/snippet), even with stop_reason=end_turn.
# Retry a few times before giving up, since re-sampling usually produces valid
# JSON. `call` is a zero-arg closure so callers keep their own Bedrock
# invocation shape (invoke vs invoke_cached) without this helper knowing
# about either.
def invoke_parsed(call: Callable[[], str], model: type[T], label: str = "") -> T:
    last_error: ValidationError | None = None
    for attempt in range(1, MAX_PARSE_ATTEMPTS + 1):
        response = call()
        try:
            return model.model_validate_json(response)
        except ValidationError as e:
            last_error = e
            logger.warning("invalid %s JSON: %s attempt=%d/%d", model.__name__, label, attempt, MAX_PARSE_ATTEMPTS)

    raise last_error
