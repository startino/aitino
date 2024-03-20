import math
import os
import random
from typing import Type

from dotenv import load_dotenv
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain.agents import Tool
from langchain_community.utilities import SerpAPIWrapper

load_dotenv()

key = os.environ.get("SERPAPI_API_KEY")
web_scrape = SerpAPIWrapper(serpapi_api_key=key) # "10610c34e50e1784e6cef9f2741d65917c7bd2fb"

class ScraperToolInput(BaseModel):
    query: str = Field(title="Query", description="The content that will be queried for")


class ScraperTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = ScraperToolInput
    def __init__(self):
        super().__init__(
            name="scraper_tool",
            func=web_scrape.run,
            description="scrapes web with serper"
        )


class CircumferenceToolInput(BaseModel):
    radius: float = Field()


class CircumferenceTool(BaseTool):
    name = "circumference_calculator"
    description = "Use this tool when you need to calculate a circumference using the radius of a circle"
    args_schema: Type[BaseModel] = CircumferenceToolInput

    def _run(self, radius: float):
        return float(radius) * 2.0 * math.pi


def get_file_path_of_example():
    # Get the current working directory
    current_dir = os.getcwd()

    # Go one directory up
    # parent_dir = os.path.dirname(current_dir)

    # Move to the target directory
    target_folder = os.path.join(current_dir, "src/tooling/test_files")

    # Construct the path to your target file
    # file_path = os.path.join(target_folder, "test_files/radius.txt")

    return os.path.join(target_folder, random.choice(os.listdir(target_folder)))
