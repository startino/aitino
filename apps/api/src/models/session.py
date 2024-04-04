from datetime import UTC, datetime
from enum import StrEnum, auto
from typing import Literal, Protocol
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.models.rate_limit import RateLimitResponse


class SessionStatus(StrEnum):
    RUNNING = auto()
    FINISHED = auto()
    IDLE = auto()


class SessionBase(BaseModel):
    crew_id: UUID
    profile_id: UUID
    title: str | None

    class Config:
        mode = "json"


class Session(SessionBase):
    id: UUID = Field(default_factory=lambda: uuid4())
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    status: SessionStatus = SessionStatus.RUNNING


class SessionRequest(SessionBase):
    pass


class SessionResponse(Session):
    pass


class SessionUpdate(SessionBase):
    crew_id: UUID | None = None
    profile_id: UUID | None = None
    title: str | None = None
    status: SessionStatus | None = None


class RunRequestModel(BaseModel):
    id: UUID
    profile_id: UUID
    session_title: str = "Untitled"
    session_id: UUID | None = None
    reply: str | None = None


class RunResponseModel(BaseModel):
    status: Literal["success"] | Literal["failure"]
    session: Session
    rate_limit_data: RateLimitResponse
