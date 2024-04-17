from datetime import UTC, datetime
from enum import StrEnum, auto
from typing import Literal, Protocol
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SessionStatus(StrEnum):
    RUNNING = auto()
    FINISHED = auto()
    IDLE = auto()


class Session(BaseModel):
    id: UUID 
    created_at: datetime
    profile_id: UUID
    reply: str 
    crew_id: UUID
    title: str 
    last_opened_at: datetime 
    status: SessionStatus 


class SessionInsertRequest(BaseModel):
    crew_id: UUID
    profile_id: UUID
    title: str | None


class SessionUpdateRequest(BaseModel):
    crew_id: UUID | None = None
    reply: str | None = None
    profile_id: UUID | None = None
    title: str | None = None
    status: SessionStatus | None = None


class SessionRunRequest(BaseModel):
    crew_id: UUID
    profile_id: UUID
    session_title: str = "Untitled"
    session_id: UUID | None = None
    reply: str | None = None


class SessionRunResponse(BaseModel):
    status: Literal["success"] | Literal["failure"]
    session: Session | None = None


class SessionGetRequest(BaseModel):
    profile_id: UUID | None = None
    crew_id: UUID | None = None
    title: str | None = None
    status: SessionStatus | None = None