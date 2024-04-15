from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Message(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    session_id: UUID
    profile_id: UUID
    sender_id: UUID | None = None  # None means admin here
    recipient_id: UUID | None = None  # None means admin here aswell
    content: str
    role: str = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))


class MessageInsertRequest(BaseModel):
    session_id: UUID
    content: str
    role: str = "user"
    recipient_id: UUID | None = None  # None means admin here aswell
    sender_id: UUID | None = None  # None means admin here
    profile_id: UUID


class MessageUpdateRequest(BaseModel):
    session_id: UUID | None = None
    content: str | None = None
    role: str | None = None
    recipient_id: UUID | None = None 
    sender_id: UUID | None = None 
    profile_id: UUID | None = None


class MessageGetRequest(BaseModel):
    session_id: UUID | None = None
    profile_id: UUID | None = None
    recipient_id: UUID | None = None 
    sender_id: UUID | None = None
