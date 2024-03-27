import os
from typing import Type

from dotenv import load_dotenv
from langchain_community.tools import BingSearchRun
from langchain_community.utilities import BingSearchAPIWrapper
from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

load_dotenv()

#key = os.environ.get("BING_SUBSCRIPTION_KEY")
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"

ID = "71e4ddcc-4475-46f2-9816-894173b1292e"


class BingToolInput(BaseModel):
    query: str = Field(title="Query", description="Search query input to search bing")

class BingTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = BingToolInput

    def __init__(self, api_key):
        bing_tool = BingSearchRun(api_wrapper=BingSearchAPIWrapper(bing_subscription_key=api_key))
        super().__init__(
            name="bing_search",
            func=bing_tool.run,
            description="""A wrapper around Bing Search. 
            Useful for when you need to answer questions about current events. 
            Input should be a search query.""",
        )
 
