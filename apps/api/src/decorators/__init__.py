from functools import wraps
import aioredis
from fastapi import HTTPException
from src.interfaces.redis import get_redis
from src.interfaces.db import supabase


class RateLimit:
    async def init_redis(self):
        self.redis = await aioredis.create_redis("redis://localhost")
    def limit(self):
        async def decorator(func):
            async def wrapper(profile_id: str, *args, **kwargs):
                redis = await get_redis()
                key = f"rate_limit:{profile_id}"
                current_requests = await redis.incr(key)
                tier_id = (
                    supabase.table("profiles")
                    .select("tier_id")
                    .eq("id", profile_id)
                    .maybe_single()
                    .execute()
                )
                if not tier_id:
                    raise HTTPException(status_code=401, detail="Could not find profile")
                tier = (
                    supabase.table("tiers")
                    .select("period", "limit")
                    .eq("id", tier_id)
                    .maybe_single()
                    .execute()
                )
                if not tier:
                    raise HTTPException(status_code=404, detail="Tier not found")
                limit = tier.data["limit"]
                period = tier.data["period"]
                if current_requests > limit:
                    raise HTTPException(status_code=429, detail="Rate limit exceeded")
                if current_requests == 1:
                    await redis.expire(key, period * 3600)
                return await func(profile_id, *args, **kwargs)

            return wrapper

        return decorator
