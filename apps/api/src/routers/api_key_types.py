import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.interfaces import db
from src.models import (
    APIKeyTypeResponseModel,
)

router = APIRouter(prefix="/api_key_types", tags=["api key types"])

logger = logging.getLogger("root")


@router.get("/")
def get_all_api_key_types() -> list[APIKeyTypeResponseModel]:
    return db.get_api_key_types()