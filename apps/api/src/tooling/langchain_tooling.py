# import autogen
import logging
import os
from enum import StrEnum
from typing import Any, Type

from langchain.tools.file_management.read import ReadFileTool
from langchain_community.tools.file_management import MoveFileTool
from langchain_core.tools import BaseTool

from .tools.tools import ScraperTool

logger = logging.getLogger("root")


class ToolOptions(StrEnum):
    MOVE_FILE_TOOL = "f57d47fd-5783-4aac-be34-17ba36bb6242"
    READ_FILE_TOOL = "ca16f5dd-c17f-4231-a3e6-4b6ddf2f3d67"
    SCRAPER_TOOL = "4ac25953-dc41-42d5-b9f2-bcae3b2c1d9f"

    INVALID = ""



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
    match (tool):
        case ToolOptions.MOVE_FILE_TOOL:
            return MoveFileTool()
        case ToolOptions.READ_FILE_TOOL:
            return ReadFileTool()
        case ToolOptions.SCRAPER_TOOL:
            return ScraperTool()
        case ToolOptions.INVALID:
            return None


if __name__ == "__main__":
    tools = [
        "f57d47fd-5783-4aac-be34-17ba36bb6242",
        "ca16f5dd-c17f-4231-a3e6-4b6ddf2f3d67",
        "4ac25953-dc41-42d5-b9f2-bcae3b2c1d9f",
    ]
    generated_tools = []
    for tool in tools:
        tool = generate_tool_from_uuid(tool)
        if tool is None:
            print("fail")
        else:
            print("cool, ", tool.name)
            generated_tools.append(tool)

    print(generate_llm_config(generated_tools))
