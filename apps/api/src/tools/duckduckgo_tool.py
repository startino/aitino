import logging
from typing import Callable, Optional, Type

from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities.duckduckgo_search import (
    DuckDuckGoSearchAPIWrapper,
)

ID = "7dc53d81-cdac-4320-8077-1a7ab9497551"

logger = logging.getLogger("root")


class DuckDuckGoSearchToolInput(BaseModel):
    tool_input: str = Field(
        title="query", description="Search query input to look up on duck duck go"
    )
    region: str = Field(
        title="region", description="Region to use for the search", default="wt-wt"
    )
    source: str = Field(
        title="source",
        description="Source of information, ex 'text' or 'news'",
        default="text",
    )


class DuckDuckGoSearchTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = DuckDuckGoSearchToolInput

    def __init__(self):
        super().__init__(
            name="duck_duck_go_search",
            func=self._run,
            description="""search the internet through the search engine duck duck go""",
        )

    def _run(
        self, tool_input: str, region: str = "wt-wt", source: str = "text"
    ) -> Callable:
        """Method passed to agent so the agent can initialize the wrapper with additional args"""
        logger.debug("Creating DuckDuckGo wrapper")
        ddgs_tool = DuckDuckGoSearchRun(
            wrapper=DuckDuckGoSearchAPIWrapper(region=region, source=source)
        )

        return ddgs_tool.run(tool_input=tool_input)
