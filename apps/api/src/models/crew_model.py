from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel

from .agent_model import AgentModel


class CrewBaseModel(BaseModel):
    receiver_id: UUID


class CrewModel(CrewBaseModel):
    delegator_id: UUID | None = (
        None  # None means admin again, so its the original crew (has no parent crew)
    )
    agents: list[AgentModel]
    sub_crews: list[CrewModel] = (
        []
    )  # Must set delegator_id for each sub_crew in sub_crews


class CrewRequestModel(CrewBaseModel):
    prompt: dict
    profile_id: UUID
    edges: list[dict]
    published: bool
    title: str
    description: str
    nodes: list[str]


class CrewUpdateModel(BaseModel):
    receiver_id: UUID | None = None
    prompt: dict | None = None
    profile_id: UUID | None = None
    edges: list[dict] | None = None
    published: bool | None = None
    title: str | None = None
    description: str | None = None
    nodes: list[str] | None = None

    class Config:
        exclude_none = True


class CrewResponseModel(BaseModel):
    id: UUID
    profile_id: UUID
    edges: list[dict]
    published: bool
    title: str
    description: str
    nodes: list[str]
    receiver_id: UUID | None = None
    avatar: str | None = None
    prompt: dict | None = None
