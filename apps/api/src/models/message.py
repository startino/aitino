from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Message(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    session_id: UUID
    profile_id: UUID
    sender_id: UUID | None = None
    recipient_id: UUID | None = None
    content: str
    role: str = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
