from pydantic import BaseModel, Field
from datetime import datetime, UTC
from typing import Optional
from uuid import uuid4, UUID


class SavedSubmission(BaseModel):
    """
    A Reddit submission that has been saved to the database.
    It's a variation of the EvaluatedSubmission but with the submission
    expanded to include the title and body.
    """

    id: UUID = Field(default_factory=lambda: uuid4())
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    reddit_id: str
    title: str
    body: str
    url: str
    is_relevant: bool
    reason: Optional[str]
    cost: float
    qualifying_question: Optional[str]
