from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from .agent_model import Agent


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
    published: bool
    title: str
    description: str
    updated_at: datetime
    agents: list[UUID]
    receiver_id: UUID | None = None
    avatar: str
    prompt: str


class ValidCrew(BaseModel):
    id: UUID
    created_at: datetime
    profile_id: UUID
    published: bool
    title: str
    description: str
    updated_at: datetime
    agents: list[UUID]
    receiver_id: UUID
    avatar: str
    prompt: str


class CrewInsertRequest(BaseModel):
    receiver_id: UUID | None = None
    prompt: str = ""
    profile_id: UUID
    published: bool
    title: str = ""
    description: str = ""
    agents: list[UUID] = []


class CrewUpdateRequest(BaseModel):
    receiver_id: UUID | None = None
    prompt: str | None = None
    profile_id: UUID | None = None
    published: bool | None = None
    title: str | None = None
    description: str | None = None
    agents: list[UUID] | None = None


class CrewGetRequest(BaseModel):
    profile_id: UUID | None = None
    receiver_id: UUID | None = None
    title: str | None = None
    published: bool | None = None
