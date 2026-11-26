from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from copilot.agents.base import BaseAgent
from copilot.llm.wrappers import with_tools
from copilot.tools.web_search import web_search_tool

RESEARCHER_SYSTEM_PROMPT = """You are an expert AI Research Assistant.
Your job is to gather accurate, well-sourced information for the given research query.
Use the `web_search` tool to find current, authoritative sources.
Always cite source URLs when summarizing your findings.
Be concise, factual, and avoid speculation."""


class ResearchOutput(BaseModel):
    query: str = Field(..., description="The original research query")
    summary: str = Field(..., description="Synthesized research findings with inline citations")
    tool_calls_made: int = Field(default=0, description="Number of tool calls executed")


class ResearcherAgent(BaseAgent):
    """Single tool-calling agent that researches a topic using web search."""

    name: str = "researcher"

    def __init__(
        self,
        llm: BaseChatModel,
        tools: list[BaseTool] | None = None,
        max_tool_rounds: int = 3,
    ) -> None:
        super().__init__(llm = llm)
        self.tools: list[BaseTool] = tools if tools is not None else [web_search_tool]
        self.tool_map: dict[str, BaseTool] = {t.name: t for t in self.tools}
        self.max_tool_rounds = max_tool_rounds

    async def run(self, query: str) -> ResearchOutput:
        """Run the researcher tool-calling loop for a given query."""
        llm_with_tools = with_tools(self.llm, self.tools)
        messages: list[BaseMessage] = [
            SystemMessage(content=RESEARCHER_SYSTEM_PROMPT),
            HumanMessage(content=f"Research the following topic thoroughly:\n\n{query}"),
        ]

        tool_calls_made = 0

        for _ in range(self.max_tool_rounds):
            response = await llm_with_tools.ainvoke(messages)
            messages.append(response)

            if not isinstance(response, AIMessage) or not response.tool_calls:
                return ResearchOutput(
                    query=query,
                    summary=str(response.content),
                    tool_calls_made=tool_calls_made,
                )

            for call in response.tool_calls:
                tool_name = call["name"]
                tool_args = call["args"]
                tool_id = call["id"] or ""

                selected_tool = self.tool_map.get(tool_name)
                if selected_tool is None:
                    result = f"Error: Tool '{tool_name}' is not available."
                else:
                    result = str(await selected_tool.ainvoke(tool_args))
                    tool_calls_made += 1

                messages.append(ToolMessage(content=result, tool_call_id=tool_id))

        # Final synthesis pass if tool rounds were exhausted
        final_response = await self.llm.ainvoke(messages)
        return ResearchOutput(
            query=query,
            summary=str(final_response.content),
            tool_calls_made=tool_calls_made,
        )