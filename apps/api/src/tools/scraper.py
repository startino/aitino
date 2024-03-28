import os
from typing import Type

from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.utilities import SerpAPIWrapper

load_dotenv()

ID = "4ac25953-dc41-42d5-b9f2-bcae3b2c1d9f"
API_KEY_TYPE = "3b64fe26-20b9-4064-907e-f2708b5f1656"

# key = os.environ.get("SERPAPI_API_KEY")


class ScraperToolInput(BaseModel):
    query: str = Field(
        title="Query", description="The content that will be queried for"
    )


class ScraperTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = ScraperToolInput

    def __init__(self, api_key):
        web_scrape = SerpAPIWrapper(serpapi_api_key=api_key)
        super().__init__(
            name="scraper_tool",
            func=web_scrape.run,
            description="scrapes web with serper",
        )
