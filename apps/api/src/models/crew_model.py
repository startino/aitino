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
    sub_crews: list["CrewModel"] = (
        []
    )  # Must set delegator_id for each sub_crew in sub_crews


class CrewRequestModel(CrewBaseModel):
    prompt: dict
    profile_id: UUID
    edges: list[dict]
    published: bool
    title: str
    description: str
    nodes: list[dict]
