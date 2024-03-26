from datetime import UTC, datetime
from enum import StrEnum, auto
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SessionStatus(StrEnum):
    RUNNING = auto()
    FINISHED = auto()
    IDLE = auto()


class Session(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    crew_id: UUID
    profile_id: UUID
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    status: SessionStatus = SessionStatus.RUNNING

class SessionUpdate(BaseModel):
    id: UUID | None = None
    crew_id: UUID | None = None
    profile_id: UUID | None = None
    title: str | None = None
    status: SessionStatus | None = None
