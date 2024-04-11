from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class AgentBaseModel(BaseModel):
    title: str
    role: str
    system_message: str
    tools: list[dict]
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo-preview"]


class AgentRequestModel(AgentBaseModel):
    description: str | None = None
    profile_id: UUID
    version: str | None = None
    avatar: str


class Agent(AgentRequestModel):
    id: UUID
    created_at: datetime
    published: bool


class AgentUpdateModel(AgentRequestModel):
    title: str | None = None
    role: str | None = None
    system_message: str | None = None
    tools: list[dict] | None = None
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo-preview"] | None = None
    description: str | None = None
    profile_id: UUID | None = None
    version: str | None = None
    avatar: str | None = None
