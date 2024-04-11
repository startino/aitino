import logging
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, HTTPException

from src.interfaces import db
from src.models import CrewRequestModel, Crew, CrewUpdateModel

router = APIRouter(
    prefix="/crews",
    tags=["crews"],
)

logger = logging.getLogger("root")


@router.post("/", status_code=201)
def insert_crew(crew: CrewRequestModel) -> Crew:
    if not db.get_profile_from_id(crew.profile_id):
        raise HTTPException(404, "profile not found")
    return db.insert_crew(crew)


@router.get("/")  # /crews/?by_profile=profile_id
def get_crews_of_user(by_profile: UUID, ascending: bool = False) -> list[Crew]:
    return db.get_user_crews(by_profile, ascending)


@router.get("/published")
def get_published_crews() -> list[Crew]:
    return db.get_published_crews()


@router.patch("/{crew_id}")
def update_crew(crew_id: UUID, content: CrewUpdateModel) -> Crew:
    logger.debug(content.model_dump())
    if not db.get_crew_from_id(crew_id):
        raise HTTPException(404, "crew not found")

    return db.update_crew(crew_id, content)


@router.get("/{crew_id}")
def get_crew_by_id(crew_id: UUID) -> Crew:
    return db.get_crew_from_id(crew_id)


@router.delete("/{crew_id}")
def delete_crew(crew_id: UUID) -> Crew:
    return db.delete_crew(crew_id)