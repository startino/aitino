import inspect
import logging
import os
import random
from typing import Any
from uuid import UUID

from dotenv import load_dotenv
from langchain_core.tools import BaseTool
from src.interfaces import db
from src.models import Tools

from src.tools.alpha_vantage import ID as ALPHA_VANTAGE_TOOL_ID
from src.tools.alpha_vantage import AlphaVantageTool
from src.tools.arxiv_tool import ID as ARXIV_TOOL_ID
from src.tools.arxiv_tool import ArxivTool
from src.tools.bing import ID as BING_SEARCH_TOOL_ID
from src.tools.bing import BingTool
from src.tools.brave_search import ID as BRAVE_TOOL_ID
from src.tools.brave_search import BraveSearchTool
from src.tools.duckduckgo_tool import ID as DDGS_TOOL_ID
from src.tools.duckduckgo_tool import DuckDuckGoSearchTool
from src.tools.google_serper import RESULTS_ID as GOOGLE_SERPER_RESULTS_TOOL_ID
from src.tools.google_serper import RUN_ID as GOOGLE_SERPER_RUN_TOOL_ID
from src.tools.google_serper import GoogleSerperResultsTool, GoogleSerperRunTool
from src.tools.move_file import ID as MOVE_TOOL_ID
from src.tools.move_file import MoveFileTool
from src.tools.read_file import ID as READ_TOOL_ID
from src.tools.read_file import ReadFileTool
from src.tools.scraper import ID as SCRAPER_TOOL_ID
from src.tools.scraper import ScraperTool
from src.tools.stackapi_tool import ID as STACKAPI_ID
from src.tools.stackapi_tool import StackAPISearchTool
from src.tools.wikipedia_tool import ID as WIKIPEDIA_TOOL_ID
from src.tools.wikipedia_tool import WikipediaTool

tools: dict = {
    ARXIV_TOOL_ID: ArxivTool,
    READ_TOOL_ID: ReadFileTool,
    MOVE_TOOL_ID: MoveFileTool,
    SCRAPER_TOOL_ID: ScraperTool,
    ALPHA_VANTAGE_TOOL_ID: AlphaVantageTool,
    WIKIPEDIA_TOOL_ID: WikipediaTool,
    BING_SEARCH_TOOL_ID: BingTool,
    DDGS_TOOL_ID: DuckDuckGoSearchTool,
    GOOGLE_SERPER_RUN_TOOL_ID: GoogleSerperRunTool,
    GOOGLE_SERPER_RESULTS_TOOL_ID: GoogleSerperResultsTool,
    BRAVE_TOOL_ID: BraveSearchTool,
    STACKAPI_ID: StackAPISearchTool,
}

logger = logging.getLogger("root")
load_dotenv()


def get_file_path_of_example() -> str:
    current_dir = os.getcwd()
    target_folder = os.path.join(current_dir, "src/tools/test_files")

    return os.path.join(target_folder, random.choice(os.listdir(target_folder)))


def generate_llm_config(tools: list[BaseTool]) -> list[dict]:
    """Generate a valid function schema for the autogen llm config from the given tool."""
    schemas = []
    for tool in tools:
        function_schema = {
            "name": tool.name.lower().replace(" ", "_"),
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }

        if tool.args is not None:
            function_schema["parameters"]["properties"] = tool.args
        schemas.append(function_schema)

    return schemas


def get_tool_ids_from_agent(tools: list[dict[str, Any]]) -> list[str]:
    return [tool["id"] for tool in tools]


def has_param(cls, param_name) -> bool:
    init_signature = inspect.signature(cls.__init__)
    return param_name in init_signature.parameters


def generate_tool_from_uuid(
    tool: str, api_key_types: dict[str, str], api_keys: dict[str, str]
) -> BaseTool | None:
    for tool_id in tools:
        if tool_id == tool:
            tool_key_type = ""
            tool_cls = tools[tool_id]
            api_key = None
            if tool in api_key_types.keys():
                # set the api_key_type to the current tools api_key_type (the api_key_types dict has key "tool_id" and value "api_key_type_id")
                tool_key_type = api_key_types[tool]
                if tool_key_type in api_keys.keys():
                    # set current api key that will be given to current tool (the api_keys dict has key "api_key_type_íd" and value "api_key")
                    api_key = api_keys[tool_key_type]

            if has_param(tool_cls, "api_key"):
                logger.info("has parameter 'api_key'")
                if not api_key:
                    raise TypeError(
                        "api key should not be none when passed to tool that needs api key"
                    )
                tool_object = tools[tool_id](api_key=api_key)
                logger.info("creating tool")
                return tool_object

            logger.info("making tool without api_key")
            return tool_cls()

    return None


if __name__ == "__main__":
    serpapi_key = os.environ.get("SERPAPI_API_KEY")
    bing_key = os.environ.get("BING_SUBSCRIPTION_KEY")
    alphavantage_key = os.environ.get("ALPHAVANTAGE_API_KEY")
    google_search_key = os.environ.get("GOOGLE_SEARCH_API_KEY")
    brave_search_key = os.environ.get("BRAVE_API_KEY")
    print(serpapi_key, bing_key, alphavantage_key, google_search_key)
    if not all([serpapi_key, bing_key, alphavantage_key, google_search_key]):
        raise TypeError("a key was not found in env variables")

    api_keys = {
        "3b64fe26-20b9-4064-907e-f2708b5f1656": serpapi_key,
        "5281bbc4-45ea-4f4b-b790-e92c62bbc019": bing_key,
        "8a29840f-4748-4ce4-88e6-44e1ef5b7637": alphavantage_key,
        "4d950712-8b4c-4cc0-a24d-7599638119f2": google_search_key,
        "58dc6249-3a0c-496b-91f3-27cf0054bfb0": brave_search_key,
    }
    api_key_types = {
        "fa4c2568-00d9-4e3c-9ab7-44f76f3a0e3f": "8a29840f-4748-4ce4-88e6-44e1ef5b7637",  # alpha vantage
        "4ac25953-dc41-42d5-b9f2-bcae3b2c1d9f": "3b64fe26-20b9-4064-907e-f2708b5f1656",  # serpapi
        "71e4ddcc-4475-46f2-9816-894173b1292e": "5281bbc4-45ea-4f4b-b790-e92c62bbc019",  # bing search
        "3e2665a8-6d73-42ee-a64f-50ddcc0621c6": "4d950712-8b4c-4cc0-a24d-7599638119f2",  # google search (run)
        "1046fefb-a540-498f-8b96-7292523559e0": "4d950712-8b4c-4cc0-a24d-7599638119f2",  # google search (results)
        "3c0d3635-80f4-4286-aab6-c359795e1ac4": "58dc6249-3a0c-496b-91f3-27cf0054bfb0",  # brave search
    }
    agents_tools = [
        "f57d47fd-5783-4aac-be34-17ba36bb6242",  # Move File Tool
        "ca16f5dd-c17f-4231-a3e6-4b6ddf2f3d67",  # Read File Tool
        "4ac25953-dc41-42d5-b9f2-bcae3b2c1d9f",  # Scraper Tool
        "bb207b0c-e998-4a40-9508-ec37dd195b0c",  # Arxiv Tool
        "fa4c2568-00d9-4e3c-9ab7-44f76f3a0e3f",  # Alpha Vantage Tool
        "243f1c6b-dfc5-4d64-ab7f-331e74858393",  # Wikipedia Tool
        "7dc53d81-cdac-4320-8077-1a7ab9497551",  # DuckDuckGoSearch Tool
        "3e2665a8-6d73-42ee-a64f-50ddcc0621c6",  # Google Serper Run
        "1046fefb-a540-498f-8b96-7292523559e0",  # Google Serper Results
        "3c0d3635-80f4-4286-aab6-c359795e1ac4",  # Brave search
        "612ddae6-ecdd-4900-9314-1a2c9de6003d",  # StackAPI
    ]
    generated_tools = []
    for tool in agents_tools:
        tool = generate_tool_from_uuid(tool, api_key_types, api_keys)  # type: ignore
        if tool is None:
            print("fail")
        else:
            print("cool, ", tool.name)
            generated_tools.append(tool)

    print(generate_llm_config(generated_tools))
   