from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Message(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    session_id: UUID
    recipient: str
    content: str
    role: str  # TODO: Convert to Literal ("user", "system", "tool", ...)
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
