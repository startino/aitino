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
    title: str | None
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    status: SessionStatus = SessionStatus.RUNNING


class RunRequestModel(BaseModel):
    id: UUID
    profile_id: UUID
    session_title: str = "Untitled"
    session_id: UUID | None = None
    reply: str | None = None