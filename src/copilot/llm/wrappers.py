from collections.abc import Sequence
from typing import TypeVar

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

def with_structured_output(
    llm: BaseChatModel,
    schema: type[T],
) -> Runnable[Sequence[BaseMessage], T]:
    """Return a runnable that enforces a Pydantic schema on the model's response."""
    return llm.with_structured_output(schema)  # type: ignore[return-value]



def with_tools(
    llm: BaseChatModel,
    tools: Sequence[BaseTool],
)-> Runnable[Sequence[BaseMessage],BaseMessage]:
    """Binding Langchain tools to a chatmodel."""
    return llm.bind_tools(tools)

