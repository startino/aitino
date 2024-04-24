from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class Tools(BaseModel):
    id: UUID
    parameter: dict
    # will fix typing on this eventually, rn it's just gonna be dict


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
    # had to remove the "list[Tools]" type, since it wasn't being formatted properly
    # i gotta find a solution to that eventually, but this works for now
    description: str
    role: str
    version: str


class AgentInsertRequest(BaseModel):
    profile_id: UUID
    title: str
    role: str
    system_message: str
    published: bool
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo"]
    tools: list[dict]
    avatar: str = ""
    description: str = ""
    version: str = ""


class AgentUpdateRequest(BaseModel):
    profile_id: UUID | None = None
    avatar: str | None = None
    title: str | None = None
    role: str | None = None
    system_message: str | None = None
    published: bool | None = None
    model: Literal["gpt-3.5-turbo", "gpt-4-turbo"] | None = None
    tools: list[dict] | None = None
    description: str | None = None
    version: str | None = None


class AgentGetRequest(BaseModel):
    profile_id: UUID | None = None
    published: bool | None = None
