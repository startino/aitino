import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.interfaces import db
from src.models import APIKeyProvider

router = APIRouter(prefix="/api-key-provider", tags=["api key provider"])

logger = logging.getLogger("root")


@router.get("/")
def get_all_api_key_provider() -> list[APIKeyProvider]:
    return db.get_api_key_provider()
