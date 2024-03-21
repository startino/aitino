from datetime import UTC, datetime
from enum import StrEnum, auto
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SessionStatus(StrEnum):
    RUNNING = auto()
    FINISHED = auto()
    CANCELLED = auto()


class Session(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    crew_id: UUID
    profile_id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    status: SessionStatus = SessionStatus.RUNNING
