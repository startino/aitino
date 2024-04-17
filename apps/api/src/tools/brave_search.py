import logging
from typing import Callable, Optional, Type

from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.tools import BraveSearch

ID = "3c0d3635-80f4-4286-aab6-c359795e1ac4"

logger = logging.getLogger("root")


class BraveSearchToolInput(BaseModel):
    tool_input: str = Field(
        title="query", description="Search query input to look up on brave"
    )


class BraveSearchTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = BraveSearchToolInput

    def __init__(self, api_key):
        tool = BraveSearch.from_api_key(api_key=api_key, search_kwargs={"count": 3})
        super().__init__(
            name="brave_search",
            func=tool.run,
            description="""search the internet through the search engine brave""",
        )
