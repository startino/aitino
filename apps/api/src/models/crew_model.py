from uuid import UUID

from pydantic import BaseModel

from .agent import Agent


class CrewModel(BaseModel):
    receiver_id: UUID
    delegator_id: UUID | None = (
        None  # None means admin again, so its the original crew (has no parent crew)
    )
    agents: list[Agent]
    sub_crews: list["CrewModel"] = (
        []
    )  # Must set delegator_id for each sub_crew in sub_crews
