import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.interfaces import db
from src.models import CrewInsertRequest, Crew, CrewUpdateRequest, CrewGetRequest

router = APIRouter(
    prefix="/crews",
    tags=["crews"],
)

logger = logging.getLogger("root")


@router.get("/")
def get_crews(q: CrewGetRequest = Depends()) -> list[Crew]:
    return db.get_crews(q.profile_id, q.receiver_id, q.title, q.published)


@router.post("/", status_code=201)
def insert_crew(crew: CrewInsertRequest) -> Crew:
    if not db.get_profile(crew.profile_id):
        raise HTTPException(404, "profile not found")
    return db.insert_crew(crew)


@router.patch("/{crew_id}")
def update_crew(crew_id: UUID, content: CrewUpdateRequest) -> Crew:
    logger.debug(content.model_dump())
    if not db.get_crew(crew_id):
        raise HTTPException(404, "crew not found")

    return db.update_crew(crew_id, content)


@router.get("/{crew_id}")
def get_crew_by_id(crew_id: UUID) -> Crew:
    response = db.get_crew(crew_id)
    if not response:
        raise HTTPException(404, "Crew not found")

    return response


@router.delete("/{crew_id}")
def delete_crew(crew_id: UUID) -> Crew:
    return db.delete_crew(crew_id)
