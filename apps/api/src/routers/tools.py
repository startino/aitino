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
    prefix="/tools",
    tags=["tools"],
)


@router.patch("/{agent_id}")
def add_tool(agent_id: UUID, tool_id: UUID) -> Agent:
    if not db.get_agent(agent_id):
        raise HTTPException(404, "agent not found")

    return db.update_agent_tool(agent_id, tool_id)
