from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class Agent(BaseModel):
    description: str | None = None
    profile_id: UUID
    version: str | None = None
    avatar: str
    id: UUID
    created_at: datetime
    published: bool
    title: str
    role: str
    system_message: str
    tools: list[dict]
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo-preview"]


class AgentInsertRequest(BaseModel):
    title: str
    role: str
    system_message: str
    tools: list[dict]
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo-preview"]
    description: str | None = None
    profile_id: UUID
    version: str | None = None
    avatar: str


class AgentUpdateModel(BaseModel):
    title: str | None = None
    role: str | None = None
    system_message: str | None = None
    tools: list[dict] | None = None
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo-preview"] | None = None
    description: str | None = None
    profile_id: UUID | None = None
    version: str | None = None
    avatar: str | None = None
    published: bool | None = None
