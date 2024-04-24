from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.interfaces import db
from src.models import (
    Agent,
    Tool,
    ToolGetRequest,
    ToolInsertRequest,
    ToolUpdateRequest,
)

router = APIRouter(
    prefix="/tools",
    tags=["tools"],
)


@router.get("/")
def get_tools(q: ToolGetRequest = Depends()) -> list[Tool]:
    return db.get_tools(q.name, q.api_provider_id)


@router.get("/{id}")
def get_tool(id: UUID) -> Tool:
    response = db.get_tool(id)
    if not response:
        raise HTTPException(404, "tool not found")

    return response


@router.post("/", status_code=201)
def insert_tool(tool: ToolInsertRequest) -> Tool:
    return db.insert_tool(tool)


@router.delete("/{id}")
def delete_tool(id: UUID) -> Tool:
    response = db.delete_tool(id)
    if not response:
        raise HTTPException(404, "could not find tool")

    return response


@router.patch("/{id}")
def update_tool(id: UUID, tool_update_request: ToolUpdateRequest) -> Tool:
    if not db.get_tool(id):
        raise HTTPException(404, "tool not found")

    return db.update_tool(id, tool_update_request)


@router.patch("/{agent_id}")
def add_tool(agent_id: UUID, tool_id: UUID) -> Agent:
    if not db.get_agent(agent_id):
        raise HTTPException(404, "agent not found")

    return db.update_agent_tool(agent_id, tool_id)
