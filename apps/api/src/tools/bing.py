import os
from typing import Type

from dotenv import load_dotenv
from langchain_community.tools import BingSearchRun
from langchain_community.utilities import BingSearchAPIWrapper
from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.tools.bing_search.tool import BingSearchRun
from langchain_community.utilities.bing_search import BingSearchAPIWrapper

# TODO: Split this tool into 2 different tools, like I did with the Google Serper tool, so a BingSearchRun and a BingSearchResults

BING_SEARCH_URL="https://api.bing.microsoft.com/v7.0/search"

ID = "71e4ddcc-4475-46f2-9816-894173b1292e"


class BingToolInput(BaseModel):
    tool_input: str = Field(title="Query", description="Search query input to search bing")

    #nr_of_results: int = Field(title="Number of results", description="The amount of returned results from the search", default=)


class BingTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = BingToolInput
    api_key: str = ""
    # needs to be empty string or it throws validation errors

    def __init__(self, api_key):
        #bing_tool = BingSearchRun(
        #    api_wrapper=BingSearchAPIWrapper(bing_subscription_key=api_key, bing_search_url=BING_SEARCH_URL)
        #)
        super().__init__(
            name="bing_search",
            func=self._run,
            description="""A wrapper around Bing Search. 
            Useful for when you need to answer questions about current events. 
            Input should be a search query.""",
        )
        self.api_key = api_key
    
    def _run(self, tool_input: str, nr_of_results: int = 5):
        wrapper = BingSearchAPIWrapper(
            bing_subscription_key=self.api_key,
            bing_search_url=BING_SEARCH_URL,
            k=nr_of_results,
        )
        bing_search = BingSearchRun(api_wrapper=wrapper)

        return bing_search.run(tool_input)
