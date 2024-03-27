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


@router.post("/")
def insert_crew(crew: CrewRequestModel) -> CrewResponseModel:
    if not db.get_profile_from_id(crew.profile_id):
        raise HTTPException(404, "profile not found")
    return db.insert_crew(crew)


@router.patch("/{crew_id}")
def update_crew(crew_id: UUID, content: CrewUpdateModel):
    logger.warning(content.model_dump())
    if not db.get_crew(crew_id):
        raise HTTPException(404, "crew not found")
    return db.update_crew(crew_id, content)
