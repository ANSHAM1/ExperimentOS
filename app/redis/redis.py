from typing import Any, cast

from redis.asyncio import Redis



class RedisClient:

    def __init__(self, redis_url: str) -> None:

        self.client : Redis = Redis.from_url(redis_url, decode_responses=True) # type: ignore


    async def ping(self) -> bool:

        return bool(await cast(Any, self.client).ping())


    async def close(self) -> None:

        await self.client.aclose()