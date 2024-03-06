from aioredis import from_url

redis = None
async def get_redis():
    global redis
    if not redis:
        redis = await from_url("redis://localhost")
    return redis