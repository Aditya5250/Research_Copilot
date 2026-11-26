from abc import ABC, abstractmethod
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel


class BaseAgent(ABC):
    """Abstract base class for all Copilot agents."""

    name: str = "base-agent"

    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm

    @abstractmethod
    async def run(self, *args: Any, **kwargs: Any)-> Any:
        """Executeing the agent's primary task."""
