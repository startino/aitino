from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .agent_model import Agent
from .edge import Edge

class Prompt(BaseModel):
    id: UUID
    title: str
    content: str

class CrewProcessed(BaseModel):
    receiver_id: UUID
    delegator_id: UUID | None = None
    # None means admin again, so its the original crew (has no parent crew)
    agents: list[Agent]
    sub_crews: list[Crew] = []
    # Must set delegator_id for each sub_crew in sub_crews


class Crew(BaseModel):
    id: UUID
    created_at: datetime
    profile_id: UUID
    edges: list[Edge]
    published: bool
    title: str
    description: str
    updated_at: datetime
    nodes: list[UUID]
    receiver_id: UUID | None = None
    avatar: str | None = None
    prompt: Prompt | None = None


class CrewInsertRequest(BaseModel):
    receiver_id: UUID
    prompt: Prompt
    profile_id: UUID
    edges: list[Edge]
    published: bool
    title: str
    description: str
    nodes: list[str]


class CrewUpdateRequest(BaseModel):
    receiver_id: UUID | None = None
    prompt: Prompt | None = None
    profile_id: UUID | None = None
    edges: list[Edge] | None = None
    published: bool | None = None
    title: str | None = None
    description: str | None = None
    nodes: list[str] | None = None


class CrewGetRequest(BaseModel):
    profile_id: UUID | None = None
    receiver_id: UUID | None = None
    title: str | None = None
    published: bool | None = None
