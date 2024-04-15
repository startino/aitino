import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.interfaces import db
from src.models import (
    AgentInsertRequest,
    AgentUpdateModel,
    Agent,
    AgentGetRequest,
)

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)

logger = logging.getLogger("root")


@router.get("/")
def get_agents(q: AgentGetRequest = Depends()) -> list[Agent]:
    response = db.get_agents(q.profile_id, q.crew_id, q.published)
    if not response:
        raise HTTPException(404, "crew not found or crew has no agents")
    
    return response


@router.get("/{agent_id}")
def get_agent_by_id(agent_id: UUID) -> Agent:
    agent = db.get_agent(agent_id)
    if not agent:
        raise HTTPException(404, "agent not found")

    return agent


@router.post("/")
def insert_agent(agent_request: AgentInsertRequest) -> Agent:
    if not db.get_profile(agent_request.profile_id):
        raise HTTPException(404, "profile not found")

    inserted_agent = db.insert_agent(agent_request)
    if agent_request.crew_ids:
        for crew_id in agent_request.crew_ids:
            updated_crew = db.add_agent_to_crew(crew_id, inserted_agent.id)
            if not updated_crew:
                logger.error("agent was already in crew or the crew was not found, not adding agent")
            else:
                logger.info(f"Added agent with id: {inserted_agent.id} to the crew: {crew_id}")

    return inserted_agent


@router.patch("/{agent_id}")
def patch_agent(
    agent_id: UUID, agent_update_request: AgentUpdateModel
) -> Agent:
    if not db.get_agent(agent_id):
        raise HTTPException(404, "agent not found")

    if agent_update_request.profile_id and not db.get_profile(
        agent_update_request.profile_id
    ):
        raise HTTPException(404, "profile not found")

    if agent_update_request.crew_ids:
        for crew_id in agent_update_request.crew_ids:
            updated_crew = db.add_agent_to_crew(crew_id, agent_id)
            if not updated_crew:
                logger.error("agent was already in crew or the crew was not found, not adding agent")
            else:
                logger.info(f"Added agent with id: {agent_id} to the crew: {crew_id}")

    return db.update_agents(agent_id, agent_update_request)


@router.delete("/{agent_id}")
def delete_agent(agent_id: UUID) -> Agent:
    if not db.get_agent(agent_id):
        raise HTTPException(404, "agent not found")

    return db.delete_agent(agent_id)
