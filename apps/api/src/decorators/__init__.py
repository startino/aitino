import logging
import uuid

from fastapi import HTTPException

from src.interfaces.db import supabase
from src.interfaces.redis_cache import get_redis

logger = logging.getLogger("root")


def rate_limit(profile_id: str):
    try:
        uuid.UUID(profile_id)
    except ValueError:
        raise HTTPException(status_code=403, detail="invalid profile id")

    redis = get_redis()
    key = f"rate_limit:{profile_id}"
    current_requests = redis.incr(key)
    tier_id = (
        supabase.table("profiles").select("tier_id").eq("id", profile_id).execute()
    )
    if not tier_id.data:
        raise HTTPException(status_code=401, detail="Could not find profile")

    tier = (
        supabase.table("tiers")
        .select("period", "limit")
        .eq("id", tier_id.data[0]["tier_id"])
        .execute()
    )
    if not tier:
        raise HTTPException(status_code=404, detail="Tier not found")

    limit = tier.data[0]["limit"]
    period = tier.data[0]["period"]
    if current_requests > limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    if current_requests == 1:
        redis.expire(key, period * 3600)
