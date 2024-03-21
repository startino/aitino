from langchain_core.pydantic_v1 import BaseModel, Field

class RelevanceResult(BaseModel):
    certainty: float = Field(description="A value between 0-1 to determine how certain you are that the is_relevant answer is factually correct.")
    is_relevant: bool = Field(description="Determines if the post is relevant.")
    reason: str = Field(description="Explain why you determined this as relevant or irrelevant in your answer. Only one sentence.")
