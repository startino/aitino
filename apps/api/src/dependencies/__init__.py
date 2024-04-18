import logging
import os
import uuid
from dataclasses import dataclass
from typing import Callable, cast

from dotenv import load_dotenv
from fastapi import HTTPException
from supabase import Client, create_client

from src.interfaces.redis_cache import get_redis

logger = logging.getLogger("root")

load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")


@dataclass
class RateLimitResponse:
    limit: int
    current_requests: int
    time_to_refresh: int

    @property
    def remaining_requests(self) -> int:
        return self.limit - self.current_requests

    def __dict__(self) -> dict:
        return {
            "limit": self.limit,
            "current_requests": self.current_requests,
            "time_to_refresh": self.time_to_refresh,
            "remaining_requests": self.remaining_requests,
        }


def _validate_profile_id(profile_id: str) -> str:
    """
    Validate the given profile id and returns the tier id for the profile

    returns:
        tier_id: str

    raises:
        403: Profile id is invalid UUID, 401: If the profile was not found (or tier id is not on the profile)
    """
    supabase: Client = create_client(url, key)
    try:
        uuid.UUID(profile_id)
    except ValueError:
        raise HTTPException(status_code=403, detail="invalid profile id")

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


def rate_limit_tiered(profile_id: str) -> RateLimitResponse:
    """
    Dependency for rate limiting using the subscription tier of a profile id

    args:
        profile_id: str, profile id for the querying user (rate limit and period will be given by tier of profile)
    raises:
        404: Invalid tier in given profile id, 429: Exceeded the rate limit
    """
    supabase: Client = create_client(url, key)
    redis = get_redis()
    redis_key = f"rate_limit_tiered:{profile_id}"
    current_requests = cast(int, redis.incr(redis_key))

    tier_id = _validate_profile_id(profile_id)
    tier = supabase.table("tiers").select("period", "limit").eq("id", tier_id).execute()

    if not tier:
        raise HTTPException(status_code=404, detail="Tier not found")

    limit = tier.data[0]["limit"]
    period = tier.data[0]["period"]
    if current_requests > limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    if current_requests == 1:
        redis.expire(redis_key, period * 3600)
    return RateLimitResponse(limit, current_requests, cast(int, redis.ttl(key)))


def rate_limit_profile(
    limit: int, period_seconds: int
) -> Callable[[str], RateLimitResponse]:
    """
    Dependency generator for rate limiting using profile id

    args:
        limit: int, the amount of requests that can be made to endpoint
        period_seconds: int, the period before expiration of request limitation
    returns:
        func: Callable[profile_id[str]]
    raises:
        429: Exceeded the rate limit

    """

    def func(profile_id: str) -> RateLimitResponse:
        _ = _validate_profile_id(profile_id)

        redis = get_redis()
        key = f"rate_limit:{profile_id}"
        current_requests = cast(int, redis.incr(key))

        if current_requests > limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        if current_requests == 1:
            redis.expire(key, period_seconds)
        return RateLimitResponse(limit, current_requests, cast(int, redis.ttl(key)))

    return func
