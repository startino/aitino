import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.interfaces import db
from src.models import (
    Agent,
    AgentGetRequest,
    AgentInsertRequest,
    AgentUpdateRequest,
)

router = APIRouter(
    prefix="/agents",
    tags=["agents"],
)

logger = logging.getLogger("root")


@router.get("/")
def get_agents(q: AgentGetRequest = Depends()) -> list[Agent]:
    return db.get_agents(q.profile_id, q.published)


@router.get("/{id}")
def get_agent_by_id(id: UUID) -> Agent:
    agent = db.get_agent(id)
    if not agent:
        raise HTTPException(404, "agent not found")

    return agent


@router.post("/", status_code=201)
def insert_agent(agent_request: AgentInsertRequest) -> Agent:
    if not db.get_profile(agent_request.profile_id):
        raise HTTPException(404, "profile not found")

    inserted_agent = db.insert_agent(agent_request)

    return inserted_agent


@router.patch("/{id}")
def patch_agent(id: UUID, agent_update_request: AgentUpdateRequest) -> Agent:
    if not db.get_agent(id):
        raise HTTPException(404, "agent not found")

    if agent_update_request.profile_id and not db.get_profile(
        agent_update_request.profile_id
    ):
        raise HTTPException(404, "profile not found")

    return db.update_agents(id, agent_update_request)


@router.delete("/{id}")
def delete_agent(id: UUID) -> Agent:
    if not db.get_agent(id):
        raise HTTPException(404, "agent not found")

    return db.delete_agent(id)
