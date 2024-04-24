from fastapi import APIRouter

from src.interfaces import db
from src.models import APIProvider

router = APIRouter(prefix="/api-provider", tags=["api provider"])


@router.get("/")
def get_all_api_key_provider() -> list[APIProvider]:
    return db.get_api_providers()
