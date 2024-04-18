from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class Agent(BaseModel):
    id: UUID
    created_at: datetime
    title: str
    published: bool
    profile_id: UUID
    avatar: str
    system_message: str
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo-preview"]
    tools: list[dict]
    description: str | None = None
    role: str
    version: str | None = None


class AgentInsertRequest(BaseModel):
    title: str
    profile_id: UUID
    avatar: str
    system_message: str
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo-preview"]
    tools: list[dict]
    description: str | None = None
    role: str
    version: str | None = None


class AgentUpdateModel(BaseModel):
    title: str | None = None
    published: bool | None = None
    profile_id: UUID | None = None
    avatar: str | None = None
    system_message: str | None = None
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo-preview"] | None = None
    tools: list[dict] | None = None
    version: str | None = None
    description: str | None = None
    role: str | None = None


class AgentGetRequest(BaseModel):
    profile_id: UUID | None = None
    crew_id: UUID | None = None
    published: bool | None = None
