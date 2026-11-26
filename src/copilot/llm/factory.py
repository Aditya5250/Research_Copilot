from typing import Literal

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from copilot.config import get_settings


def get_llm(
    provider: Literal["anthropic","openai"] | None = None,
    model_name: str | None =None,
    temperature: float =0.0,
)->BaseChatModel:
    """ Instantiating a configured chat model based on application setting."""
    settings=get_settings()
    selected_provider = provider or settings.default_llm_provider
    selected_model = model_name or settings.default_model_name

    if selected_provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured in environment.")
        return ChatAnthropic(
            model_name = selected_model,
            api_key = SecretStr(settings.anthropic_api_key),
            timeout = 60.0,
            stop = None
        )

    if selected_provider =="openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not configured in environment.")
        return ChatOpenAI(
            model=selected_model,
            api_key=SecretStr(settings.openai_api_key),
            temperature=temperature,
            timeout=60.0,
        )
    raise ValueError(f"unsupported LLM provider:{selected_provider}")