from datetime import UTC, datetime
from re import S
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Lead(BaseModel):
    """
    A lead represents a Redditor that has been identified as a potential client.
    """

    id: UUID = Field(default_factory=lambda: uuid4())
    submission_id: UUID
    reddit_id: str
    discovered_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    last_contacted_at: datetime | None = None
    prospect_username: str
    source: str
    last_event: str
    status: str
    data: dict
    comment: str | None = None
