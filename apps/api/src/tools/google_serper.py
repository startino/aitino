import logging
from typing import Callable, Literal, Optional, Type

from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper

RUN_ID="3e2665a8-6d73-42ee-a64f-50ddcc0621c6"

RESULTS_ID="1046fefb-a540-498f-8b96-7292523559e0"

logger = logging.getLogger("root")

class GoogleSerperRunToolInput(BaseModel):
    query: str = Field(title="query", description="search query input, looks up on google search")

class GoogleSerperResultsToolInput(BaseModel):
    query: str = Field(title="query", description="search query input, looks up on google search and returns metadata")

    nr_of_results: int = Field(title="number of results", description="number of results shown per page", default=10)

    region: str = Field(
        title="region",
        description="restricts searches to the given region and is always a two letter code, for example the USA is 'us' and Sweden is 'se'.",
        default="us",
    )
    language: str = Field(
        title="language",
        description="sets the interface language of the search, given as a two letter code, for example English is 'en' and french is 'fr'", 
        default="en",
    )
    search_type: Literal["news", "search", "places", "images"] = Field(
        title="search type",
        description="what type of content to search for, news queries through Google News, places queries Google Places etc.",
        default="search",
    )
    time_based_search: str = Field(
        title="time based search",
        description="searches at specific time frames, ex. params: qdr:h (past hour), qdr:d (past day), qdr:w (past week) etc",
        default=None,
    )


class GoogleSerperRunTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = GoogleSerperRunToolInput
    
    def __init__(self, api_key):
        search = GoogleSerperAPIWrapper(serper_api_key=api_key)
        super().__init__(
            name="google_serper_run_tool",
            func=search.run,
            description="""search the web with serper's google search api""",
        )

        
class GoogleSerperResultsTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = GoogleSerperResultsToolInput
    api_key: str = ""

    def __init__(self, api_key):
        super().__init__(
            name="google_serper_results_tool",
            func=self._run,
            description="""search the web with serper's google search api, return results with metadata""",
        )
        self.api_key = api_key

    def _run(
        self,
        query: str,
        nr_of_results: int = 10, 
        region: str = "us", 
        language: str = "en",
        search_type: Literal["news", "search", "places", "images"] = "search", 
        time_based_search: str | None = None,
    ):
        """Method passed to the agent to allow it to pass additional optional parameters, similar to the DDG search tool"""

        search = GoogleSerperAPIWrapper(
            serper_api_key=self.api_key,
            k=nr_of_results, 
            gl=region, 
            hl=language, 
            type=search_type, 
            tbs=time_based_search
        )

        return search.results(query) 
    