from typing import Any, Self, cast

from app.redis import RedisClient



class RedisCacheRepo:

    def __init__(self, client: RedisClient) -> None:

        self.client = client.client


    async def __aenter__(self) -> Self:

        return self


    async def __aexit__(self, _: type[BaseException] | None, _2: BaseException | None, _3: Any | None) -> bool:

        return False


    async def set(self, key: str, value: str, *, ex: int | None = None) -> bool:

        return bool(await self.client.set(key, value, ex=ex))


    async def get(self, key: str) -> str | None:

        return cast(str | None, await self.client.get(key))


    async def delete(self, key: str) -> int:

        return await self.client.delete(key)


    async def exists(self, key: str) -> bool:

        return bool(await self.client.exists(key))


    async def expire(self, key: str, seconds: int) -> bool:

        return await self.client.expire(key, seconds)


    async def ttl(self, key: str) -> int:

        return await self.client.ttl(key)


    async def incr(self, key: str) -> int:
        
        return await self.client.incr(key)