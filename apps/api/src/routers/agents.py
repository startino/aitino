import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.interfaces import db
from src.models import (
    AgentRequestModel,
    AgentResponseModel,
    AgentUpdateModel,
    CrewRequestModel,
    CrewResponseModel,
    CrewUpdateModel,
)

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)

logger = logging.getLogger("root")


@router.get("/published")
def get_published_agents() -> list[AgentResponseModel]:
    return db.get_published_agents()


@router.get("/by_profile")
def get_users_agents(profile_id: UUID) -> list[AgentResponseModel]:
    return db.get_users_agents(profile_id)


@router.get("/by_crew")
def get_agents_from_crew(crew_id: UUID) -> list[AgentResponseModel]:
    return db.get_agents_from_crew(crew_id)


@router.get("/{agent_id}")
def get_agent_by_id(agent_id: UUID) -> AgentResponseModel:
    agent = db.get_agent_by_id(agent_id)
    if not agent:
        raise HTTPException(404, "agent not found")

    return agent


@router.post("/")
def insert_agent(agent_request: AgentRequestModel) -> AgentResponseModel:
    if not db.get_profile_from_id(agent_request.profile_id):
        raise HTTPException(404, "profile not found")

    return db.insert_agent(agent_request)


@router.patch("/{agent_id}")
def patch_agent(
    agent_id: UUID, agent_update_request: AgentUpdateModel
) -> AgentResponseModel:
    if not db.get_agent_by_id(agent_id):
        raise HTTPException(404, "agent not found")

    if agent_update_request.profile_id and not db.get_profile_from_id(
        agent_update_request.profile_id
    ):
        raise HTTPException(404, "profile not found")

    return db.update_agents(agent_update_request)


@router.delete("/{agent_id}")
def delete_agent(agent_id: UUID) -> AgentResponseModel:
    if not db.get_agent_by_id(agent_id):
        raise HTTPException(404, "agent not found")

    return db.delete_agent(agent_id)
