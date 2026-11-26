from langchain_core.tools import tool
from pydantic import BaseModel, Field
from tavily import TavilyClient

from copilot.config import get_settings


class WebSearchResult(BaseModel):
    title: str = Field(..., description="Page title")
    url: str = Field(..., description="Source URL")
    content: str = Field(..., description="Relevant snippet from the page")
    score: float = Field(default=0.0, description="Relevance score from Tavily")


def run_tavily_search(query: str, max_results: int = 5) -> list[WebSearchResult]:
    """Executing a web search via Tavily and return structured results."""
    settings = get_settings()
    if not settings.tavily_api_key:
        raise ValueError("TAVILY_API_KEY is not configured in environment.")

    client = TavilyClient(api_key=settings.tavily_api_key)
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
    )

    results: list[WebSearchResult] = []
    for item in response.get("results", []):
        results.append(
            WebSearchResult(
                title=str(item.get("title", "Untitled")),
                url=str(item.get("url", "")),
                content=str(item.get("content", "")),
                score=float(item.get("score", 0.0)),
            )
        )
    return results


@tool("web_search")
def web_search_tool(query: str, max_results: int = 5) -> str:
    """Searching the web for up-to-date information on a topic and return cited snippets."""
    try:
        results = run_tavily_search(query=query, max_results=max_results)
    except (ValueError, ConnectionError, TimeoutError, OSError) as exc:
        return f"Web search failed: {exc}"

    if not results:
        return f"No web results found for query: {query}"

    formatted = []
    for idx, res in enumerate(results, start=1):
        formatted.append(
            f"[{idx}] {res.title}\nURL: {res.url}\nSnippet: {res.content}"
        )
    return "\n\n".join(formatted)