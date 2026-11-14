from functools import cached_property

import anthropic
from langchain_anthropic import ChatAnthropic

MODELS = ("claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5")
DEFAULT_MODEL = MODELS[0]

# ChatAnthropic always passes api_key="" to the SDK, and the SDK only loads the
# mounted Anthropic profile (ANTHROPIC_CONFIG_DIR) when api_key is None. So we
# hand it SDK clients built with no key, and auth comes from the profile.
class ProfileChatAnthropic(ChatAnthropic):
    @cached_property
    def _client(self) -> anthropic.Anthropic:
        return anthropic.Anthropic(max_retries=self.max_retries)

    @cached_property
    def _async_client(self) -> anthropic.AsyncAnthropic:
        return anthropic.AsyncAnthropic(max_retries=self.max_retries)

def chat_model(model: str = DEFAULT_MODEL) -> ProfileChatAnthropic:
    return ProfileChatAnthropic(model=model,max_tokens=4096, streaming=True, effort="low")
