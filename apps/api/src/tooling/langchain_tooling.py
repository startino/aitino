# import autogen
import logging
from enum import StrEnum
from typing import Any

from langchain.tools.file_management.read import ReadFileTool
from langchain_community.tools.file_management import MoveFileTool
from langchain_core.tools import BaseTool

logger = logging.getLogger("root")



class ToolOptions(StrEnum):
    MOVE_FILE_TOOL = "move-file-tool"
    READ_FILE_TOOL = "read-file-tool"

    @classmethod
    def from_string(cls, value):
        try:
            return cls[value.upper().replace("-", "_")]
        except KeyError:
            return cls.INVALID

    INVALID = ""


def generate_llm_config(tools: list[BaseTool]) -> list[dict]:
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


def generate_tool_from_string(tool: str) -> BaseTool | None:
    tool = ToolOptions.from_string(tool)

    match (tool):
        case ToolOptions.MOVE_FILE_TOOL:
            return MoveFileTool()
        case ToolOptions.READ_FILE_TOOL:
            return ReadFileTool()
        case ToolOptions.INVALID:
            logger.error("Tool not found")
            return None




if __name__ == "__main__":

    tool = generate_tool_from_string("move-file-tool")
    if tool is None:
        print("fail")
    else:
        print("cool", tool.name)

#get_tool_id_from_agent({})
