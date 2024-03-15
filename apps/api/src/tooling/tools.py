import os
import math
from typing import Type

from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

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
    target_folder = os.path.join(current_dir, "src/tooling")

    # Construct the path to your target file
    file_path = os.path.join(target_folder, "test_files/radius.txt")

    return file_path