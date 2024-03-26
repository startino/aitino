import logging
from uuid import UUID

from src.models.crew_model import CrewRequestModel
from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, HTTPException

from src.interfaces import db

router = APIRouter(
    prefix="/crews",
    tags=["crews"],
)

logger = logging.getLogger("root")

@router.post("/")
def add_crew(crew: CrewRequestModel):
    if not db.get_profile_from_id(crew.profile_id):
        raise HTTPException(404, "profile not found")
    db.insert_crew(crew)
    return "success"

@router.post("/update")
def update_crew(crew)
    