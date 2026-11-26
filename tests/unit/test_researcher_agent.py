from unittest.mock import AsyncMock, MagicMock

import pytest
from langchain_core.messages import AIMessage
from langchain_core.tools import tool

from copilot.agents.researcher import ResearcherAgent, ResearchOutput


@tool("web_search")
def fake_web_search(query: str) -> str:
    """Fake web search tool for unit testing."""
    return f"[1] Mock Result for {query}\nURL: https://example.com/mock\nSnippet: Mock data."


@pytest.mark.asyncio
async def test_researcher_agent_executes_tool_call_and_summarizes() -> None:
    first_ai_msg = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "web_search",
                "args": {"query": "EV battery India vs China"},
                "id": "call_123",
                "type": "tool_call",
            }
        ],
    )
    second_ai_msg = AIMessage(
        content="India and China differ in scale [https://example.com/mock]."
    )

    mock_llm_with_tools = MagicMock()
    mock_llm_with_tools.ainvoke = AsyncMock(side_effect=[first_ai_msg, second_ai_msg])

    mock_llm = MagicMock()
    mock_llm.bind_tools.return_value = mock_llm_with_tools

    agent = ResearcherAgent(llm=mock_llm, tools=[fake_web_search])
    result = await agent.run("Compare EV battery market in India vs China")

    assert isinstance(result, ResearchOutput)
    assert result.tool_calls_made == 1
    assert "https://example.com/mock" in result.summary
