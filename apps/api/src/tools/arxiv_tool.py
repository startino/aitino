from typing import Type

from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.utilities import ArxivAPIWrapper

ID = "bb207b0c-e998-4a40-9508-ec37dd195b0c"
arxiv = ArxivAPIWrapper()


class ArxivToolInput(BaseModel):
    query: str = Field(
        title="Query", description="The id for arxiv article that will be read"
    )


class ArxivTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = ArxivToolInput

    def __init__(self):
        super().__init__(
            name="arxiv_tool",
            func=arxiv.run,
            description="Returns information about an arxiv articles given id",
        )


__all__ = ["ArxivTool"]
