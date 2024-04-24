import logging
from typing import Type

from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.tools.stackexchange.tool import StackExchangeTool
from langchain_community.utilities import StackExchangeAPIWrapper

ID = "612ddae6-ecdd-4900-9314-1a2c9de6003d"

logger = logging.getLogger("root")


class StackAPIToolInput(BaseModel):
    query: str = Field(
        title="query", description="Search query input to look up on Stack Exchange"
    )


class StackAPISearchTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = StackAPIToolInput

    def __init__(self) -> None:
        tool = StackExchangeTool(api_wrapper=StackExchangeAPIWrapper())
        super().__init__(
            name="stack_api_tool",
            func=tool._run,
            description="""StackAPI searches through a network of question-and-answer (Q&A) websites""",
        )
