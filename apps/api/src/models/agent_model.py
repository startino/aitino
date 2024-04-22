from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel

class LLMModel(BaseModel):
    id: int
    name: str


class Agent(BaseModel):
    id: UUID
    created_at: datetime
    title: str
    published: bool
    profile_id: UUID
    avatar: str
    system_message: str
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo"]
    tools: list[dict]
    crew_ids: list[UUID]
    description: str
    role: str
    version: str


class AgentInsertRequest(BaseModel):
    profile_id: UUID
    avatar: str
    title: str
    role: str
    system_message: str
    published: bool
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo"]
    tools: list[dict]
    crew_ids: list[UUID]
    description: str
    version: str


class AgentUpdateModel(BaseModel):
    profile_id: UUID | None = None
    avatar: str | None = None
    title: str | None = None
    role: str | None = None
    system_message: str | None = None
    published: bool | None = None
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo"] | None = None
    tools: list[dict] | None = None
    crew_ids: list[UUID] | None = None
    description: str | None = None
    version: str | None = None


class AgentGetRequest(BaseModel):
    profile_id: UUID | None = None
    crew_id: UUID | None = None
    published: bool | None = None
