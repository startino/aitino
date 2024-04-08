import logging
from typing import Callable, Optional, Type

from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper

ID="3e2665a8-6d73-42ee-a64f-50ddcc0621c6"

logger = logging.getLogger("root")

class GoogleSerperToolInput(BaseModel):
    query: str = Field(title="query", description="search query input, looks up on google search")

class GoogleSerperTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = GoogleSerperToolInput
    
    def __init__(self, api_key):
        search = GoogleSerperAPIWrapper(serper_api_key=api_key)
        super().__init__(
            name="google_serper_tool",
            func=search.results,
            description="""search the web with serper's google search api""",
        )