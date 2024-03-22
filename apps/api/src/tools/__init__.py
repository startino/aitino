import os
import random
import logging
from typing import Any

from langchain_core.tools import BaseTool

from .arxiv import arxiv_tool, ID as ARXIV_TOOL_ID
from .read_file import ReadFileTool, ID as READ_TOOL_ID
from .scraper import ScraperTool, ID as SCRAPER_TOOL_ID
from .move_file import MoveFileTool, ID as MOVE_TOOL_ID

tools: dict[str, BaseTool] = {
    ARXIV_TOOL_ID: arxiv_tool.run(),
    READ_TOOL_ID: ReadFileTool(),
    MOVE_TOOL_ID: MoveFileTool(),
    SCRAPER_TOOL_ID: ScraperTool(),
}

logger = logging.getLogger("root")


def get_file_path_of_example():
    # Get the current working directory
    current_dir = os.getcwd()

    # Go one directory up
    # parent_dir = os.path.dirname(current_dir)

    # Move to the target directory
    target_folder = os.path.join(current_dir, "src/tools/test_files")

    # Construct the path to your target file
    # file_path = os.path.join(target_folder, "test_files/radius.txt")

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


def get_tool_id_from_agent(tools: list[dict[str, Any]]) -> list[str]:
    str_tools = []
    for tool in tools:
        str_tools.append(tool["id"])
    return str_tools


def generate_tool_from_uuid(tool: str) -> BaseTool | None:
    for tool_id in tools:
        if tool_id == tool:
            return tools[tool_id]


if __name__ == "__main__":
    agents_tools = [
        "f57d47fd-5783-4aac-be34-17ba36bb6242",
        "ca16f5dd-c17f-4231-a3e6-4b6ddf2f3d67",
        "4ac25953-dc41-42d5-b9f2-bcae3b2c1d9f",
    ]
    generated_tools = []
    for tool in agents_tools:
        tool = generate_tool_from_uuid(tool)
        if tool is None:
            print("fail")
        else:
            print("cool, ", tool.name)
            generated_tools.append(tool)

    print(generate_llm_config(generated_tools))
