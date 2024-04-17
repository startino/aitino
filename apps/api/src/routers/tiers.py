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

router = APIRouter(prefix="/tier", tags=["tier"])

logger = logging.getLogger("root")


@router.get("/")
def get_tier(q: TierGetRequest = Depends()) -> list[Tier]:
    return db.get_tiers(q.profile_id, q.stripe_tier_id)


@router.post("/")
def insert_tier(tier: TierInsertRequest) -> Tier:
    return db.insert_tier(tier)


@router.delete("/{profile_id}")
def delete_tier(profile_id: UUID) -> Tier:
    response = db.delete_tier(profile_id)
    if not response:
        raise HTTPException(404, "stripe tier id not found")

    return response


@router.patch("/{profile_id}")
def update_tier(profile_id: UUID, content: TierUpdateRequest) -> Tier:
    response = db.update_tier(profile_id, content)
    if not response:
        raise HTTPException(404, "message not found")

    return response
