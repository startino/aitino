from langchain_core.pydantic_v1 import BaseModel, Field


class RelevanceResult(BaseModel):
    is_relevant: bool = Field(description="Determines if the article is relevant.")
    reason: str = Field(
        description="Explain why you determined this article is relevant or irrelevant. Format: Article is [answer] because [reason]. Hence, it is not a lead and not relevant"
    )
