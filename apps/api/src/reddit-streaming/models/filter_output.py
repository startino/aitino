from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI

# Define your desired data structure.
class FilterOutput(BaseModel):
    answer: bool = Field(description="Answer to the yes-no question.")
    source: str = Field(description="Either the piece of text you used to answer the question or the logical reason behind it. Should be brief and only have the relevant information")
