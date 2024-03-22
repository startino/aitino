import math
from typing import Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


class CircumferenceToolInput(BaseModel):
    radius: float = Field()


class CircumferenceTool(BaseTool):
    name = "circumference_calculator"
    description = "Use this tool when you need to calculate a circumference using the radius of a circle"
    args_schema: Type[BaseModel] = CircumferenceToolInput

    def _run(self, radius: float):
        return float(radius) * 2.0 * math.pi
