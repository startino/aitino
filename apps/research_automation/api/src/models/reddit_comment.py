from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from pydantic import BaseModel as PydanticBaseModel
from typing import Optional

class RedditComment(BaseModel):
    comment: str = Field(description="the text of the reddit comment")
    # Not sure if this should be a model or simply a string.


class GenerateCommentRequest(PydanticBaseModel):
    title: str
    selftext: str
    instructions: str = ""
