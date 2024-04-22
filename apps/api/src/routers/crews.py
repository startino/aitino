import logging
from typing import Literal
from uuid import UUID


from fastapi import APIRouter, Depends, HTTPException

from src import parser
from src.interfaces import db
from src.models import (
    Crew,
    CrewGetRequest,
    CrewInsertRequest,
    CrewUpdateRequest,
)

router = APIRouter(
    prefix="/crews",
    tags=["crews"],
)

logger = logging.getLogger("root")


@router.get("/")
def get_crews(q: CrewGetRequest = Depends()) -> list[Crew]:
    return db.get_crews(q.profile_id, q.receiver_id, q.title, q.published)


@router.post("/validate/{crew_id}", status_code=200)
def validate_crew(crew_id: UUID) -> str:
    crew: Crew | None = db.get_crew(crew_id)
    if not crew:
        return "Crew not found with ID"
    _, error = parser.validate_crew(crew)

    return error


@router.post("/", status_code=201)
def insert_crew(crew: CrewInsertRequest) -> Crew:
    if not db.get_profile(crew.profile_id):
        raise HTTPException(404, "profile not found")
    
    return db.insert_crew(crew)


@router.patch("/{id}")
def update_crew(id: UUID, content: CrewUpdateRequest) -> Crew:
    logger.debug(content.model_dump())
    if not db.get_crew(id):
        raise HTTPException(404, "crew not found")

    return db.update_crew(id, content)


@router.get("/{id}")
def get_crew(id: UUID) -> Crew:
    response = db.get_crew(id)
    if not response:
        raise HTTPException(404, "Crew not found")

    return response


@router.delete("/{id}")
def delete_crew(id: UUID) -> Crew:
    return db.delete_crew(id)
