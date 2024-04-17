import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.interfaces import db
from src.models import (
    APIKeyType,
)

router = APIRouter(prefix="/api-key-types", tags=["api key types"])

logger = logging.getLogger("root")


@router.get("/")
def get_all_api_key_types() -> list[APIKeyType]:
    return db.get_api_key_types()