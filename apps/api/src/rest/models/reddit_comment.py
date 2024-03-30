from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator

class RedditComment(BaseModel):
    comment: str = Field(description="the text of the reddit comment")