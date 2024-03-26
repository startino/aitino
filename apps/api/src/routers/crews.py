import logging
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, HTTPException

from src.interfaces import db
from src.models.crew_model import CrewRequestModel

router = APIRouter(
    prefix="/crews",
    tags=["crews"],
)

logger = logging.getLogger("root")


@router.post("/")
def insert_crew(crew: CrewRequestModel):
    if not db.get_profile_from_id(crew.profile_id):
        raise HTTPException(404, "profile not found")
    db.insert_crew(crew)
    return "success"
