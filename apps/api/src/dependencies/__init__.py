import logging
import uuid
from dataclasses import dataclass
from typing import Callable, cast

from fastapi import HTTPException, Depends

from src.auth import get_current_user
from src.interfaces.db import supabase
from src.interfaces.redis_cache import get_redis
from src.models import RateLimitResponse, RunRequestModel

logger = logging.getLogger("root")


def _get_tier_from_profile_id(profile_id: uuid.UUID) -> str:
    """
    Return the tier id for a given profile id

    returns:
        tier_id: str

    raises 
        401: If the profile was not found (or tier id is not on the profile)
    """
    tier_id = (
        supabase.table("profiles").select("tier_id").eq("id", profile_id).execute()
    )
    if not tier_id.data:
        raise HTTPException(status_code=401, detail="Could not find profile")
    return tier_id.data[0]["tier_id"]


def rate_limit(limit: int, period_seconds: int, endpoint: str) -> Callable:
    """
    Dependency generator for rate limiting on a fastapi endpoint

    args:
        limit: int, the amount of requests that can be made to endpoint
        period_seconds: int, the period before expiration of request limitation
        endpoint: str, the current endpoint that depends on this function
    returns:
        func: Callable
    raises:
        429: Exceeded the rate limit
    """

    def func() -> RateLimitResponse:
        redis = get_redis()
        key = f"rate_limit:{endpoint}"
        current_requests = cast(int, redis.incr(key))

        if current_requests > limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        if current_requests == 1:
            redis.expire(key, period_seconds)
        return RateLimitResponse(limit, current_requests, cast(int, redis.ttl(key)))

    return func


def rate_limit_tiered(profile = Depends(get_current_user)) -> RateLimitResponse:
    """
    Dependency for rate limiting using the subscription tier of a profile id

    args:
        profile_id: str, profile id for the querying user (rate limit and period will be given by tier of profile)
    returns:
        response: RateLimitResponse
    raises:
        404: Invalid tier in given profile id, 429: Exceeded the rate limit
    """
    redis = get_redis()
    key = f"rate_limit_tiered:{profile.id}"
    current_requests = cast(int, redis.incr(key))

    tier_id = _get_tier_from_profile_id(profile.id)
    tier = supabase.table("tiers").select("period", "limit").eq("id", tier_id).execute()

    if not tier:
        raise HTTPException(status_code=404, detail="Tier not found")

    limit = tier.data[0]["limit"]
    period = tier.data[0]["period"]
    if current_requests > limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    if current_requests == 1:
        redis.expire(key, period * 3600)
    return RateLimitResponse(limit, current_requests, cast(int, redis.ttl(key)))


def rate_limit_profile(
    limit: int, period_seconds: int
) -> Callable:
    """
    Dependency generator for rate limiting using profile id

    args:
        limit: int, the amount of requests that can be made to endpoint
        period_seconds: int, the period before expiration of request limitation
    returns:
        func: Callable
    raises:
        429: Exceeded the rate limit

    """
    def func(profile = Depends(get_current_user)) -> RateLimitResponse:
        redis = get_redis()
        key = f"rate_limit:{profile.id}"
        current_requests = cast(int, redis.incr(key))

        if current_requests > limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        if current_requests == 1:
            redis.expire(key, period_seconds)
        return RateLimitResponse(limit, current_requests, cast(int, redis.ttl(key)))

    return func


def get_crew_id_from_body(run_request: RunRequestModel) -> str:
    return str(run_request.id)
