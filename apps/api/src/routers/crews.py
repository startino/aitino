import logging
from uuid import UUID
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, APIRouter

from src.interfaces import db


router = APIRouter(
    prefix="/crews",
    tags=["crews"],
)

logger = logging.getLogger("root")
