from unittest.mock import MagicMock, patch

import pytest

from copilot.tools.web_search import run_tavily_search, web_search_tool


def test_run_tavily_search_parses_results(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-tavily-key")
    from copilot.config import get_settings

    get_settings.cache_clear()

    mock_client = MagicMock()
    mock_client.search.return_value = {
        "results": [
            {
                "title": "EV Battery Market 2026",
                "url": "https://example.com/ev-battery",
                "content": "India and China are expanding LFP battery manufacturing.",
                "score": 0.95,
            }
        ]
    }

    with patch("copilot.tools.web_search.TavilyClient", return_value=mock_client):
        results = run_tavily_search("EV battery market India vs China")

    assert len(results) == 1
    assert results[0].title == "EV Battery Market 2026"
    assert results[0].url == "https://example.com/ev-battery"
    assert results[0].score == 0.95


def test_web_search_tool_handles_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    from copilot.config import get_settings

    get_settings.cache_clear()

    output = web_search_tool.invoke({"query": "test query"})
    assert "Web search failed" in output