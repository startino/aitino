import logging
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, HTTPException

from src.interfaces import db
from src.models import CrewRequestModel, CrewResponseModel, CrewUpdateModel

router = APIRouter(
    prefix="/crews",
    tags=["crews"],
)

logger = logging.getLogger("root")


@router.post("/", status_code=201)
def insert_crew(crew: CrewRequestModel) -> CrewResponseModel:
    if not db.get_profile_from_id(crew.profile_id):
        raise HTTPException(404, "profile not found")
    return db.insert_crew(crew)


@router.get("/{crew_id}")
def get_crew(crew_id: UUID) -> CrewResponseModel:
    return db.get_crew_from_id(crew_id)


@router.get("/")  # /crews/?by_profile=profile_id
def get_crews_of_user(by_profile: UUID, ascending: bool = False) -> list[CrewResponseModel]:
    return db.get_user_crews(by_profile, ascending)


@router.get("/published")
def get_published_crews() -> list[CrewResponseModel]:
    return db.get_published_crews()


@router.patch("/{crew_id}")
def update_crew(crew_id: UUID, content: CrewUpdateModel) -> CrewResponseModel:
    logger.debug(content.model_dump())
    if not db.get_crew_from_id(crew_id):
        raise HTTPException(404, "crew not found")

    return db.update_crew(crew_id, content)