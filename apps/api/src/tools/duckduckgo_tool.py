from typing import Type

from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun

ID="7dc53d81-cdac-4320-8077-1a7ab9497551"

class DuckDuckGoSearchToolInput(BaseModel):
    tool_input: str = Field(
        title="query", description="Search query input to look up on duck duck go"
    )


class DuckDuckGoSearchTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = DuckDuckGoSearchToolInput

    def __init__(self):
        # TODO: make wrapper take arguments from agent maybe? so it can set region, backend etc
        ddgs_tool = DuckDuckGoSearchRun(wrapper=DuckDuckGoSearchAPIWrapper())
        super().__init__(
            name="duck_duck_go_search",
            func=ddgs_tool.run,
            description="""search the internet through the search engine duck duck go""",
        )
