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
    tools: list[Tools] | list
    # the list type is just empty list, since list[Tools] requires defined fields in the db, but rn
    # if an agent doesn't use tools the "tools" field is an empty list
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
    tools: list[Tools] | list
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
    tools: list[Tools] | None = None
    description: str | None = None
    version: str | None = None


class AgentGetRequest(BaseModel):
    profile_id: UUID | None = None
    published: bool | None = None
