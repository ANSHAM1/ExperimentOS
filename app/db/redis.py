from redis.asyncio import Redis



class RedisClient:

    def __init__(self, redis_url: str) -> None:
        self.client = Redis.from_url(redis_url, decode_responses=True) # type: ignore

    async def ping(self) -> bool:
        return await self.client.ping() # type: ignore

    async def close(self) -> None:
        await self.client.aclose()