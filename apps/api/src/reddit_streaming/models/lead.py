from re import S
from pydantic import BaseModel, Field
from datetime import UTC, datetime
from uuid import UUID, uuid4

class Lead(BaseModel):
    """
    A lead represents a Redditor that has been identified as a potential client.
    """
    id: UUID = Field(default_factory=lambda: uuid4())
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    last_contacted_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    redditor: str
    source: str
    last_event: str
    status: str
    title: str
    body: str
