from langchain_core.pydantic_v1 import BaseModel, Field

class RelevanceResult(BaseModel):
    id: str =  Field(description="The id of the post")
    certainty: float = Field(description="A value between 0-1 to determine how certain you are about the is_relevant answer.")
    is_relevant: bool = Field(description="Determines if the post is relevant.")
