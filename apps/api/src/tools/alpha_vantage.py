import os
from dotenv import load_dotenv

from typing import Type
from langchain_community.utilities import AlphaVantageAPIWrapper
from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

load_dotenv()

key = os.environ.get("ALPHAVANTAGE_API_KEY")
alpha_vantage = AlphaVantageAPIWrapper(alphavantage_api_key=key)

ID = "fa4c2568-00d9-4e3c-9ab7-44f76f3a0e3f"

class AlphaVantageToolInput(BaseModel):
    from_currency: str = Field(title="From Currency", description="Currency to convert")
    to_currency: str = Field(title="To Currency", description="Currency that From Currency gets converted to")

class AlphaVantageTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = AlphaVantageToolInput

    def __init__(self):
        super().__init__(
            name="alpha_vantage_tool",
            func=alpha_vantage.run,
            description="gets currency exchange rate of two currencies",
        )

__all__ = ["AlphaVantageTool"]