import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import (
    RateLimitResponse,
    rate_limit,
    rate_limit_profile,
    rate_limit_tiered,
)
from src.interfaces import db
from src.models import (
    Tier,
    TierInsertRequest,
    TierUpdateRequest,
    TierGetRequest,
)

router = APIRouter(prefix="/tiers", tags=["tiers"])

logger = logging.getLogger("root")


@router.get("/{id}")
def get_tier(id: UUID) -> list[Tier]:
    response = db.get_tiers(id)
    if not response:
        raise HTTPException(404, "tiers information not found")

    return response


@router.post("/")
def insert_tier(tier: TierInsertRequest) -> Tier:
    return db.insert_tier(tier)


@router.delete("/{id}")
def delete_tier(id: UUID) -> Tier:
    response = db.delete_tier(id)
    if not response:
        raise HTTPException(404, "stripe tier id not found")

    return response


@router.patch("/{id}")
def update_tier(id: UUID, content: TierUpdateRequest) -> Tier:
    response = db.update_tier(id, content)
    if not response:
        raise HTTPException(404, "message not found")

    return response