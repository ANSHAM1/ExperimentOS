from typing import cast
from uuid import UUID

from app.redis import RedisClient


class SessionStore:

    def __init__(self, client: RedisClient) -> None:

        self.redis = client.client


    def _key(self, session_id: UUID) -> str:

        return f"auth:session:{session_id}"


    async def create(self, session_id: UUID, user_id: UUID, *, ttl: int) -> bool:

        return bool(
            await self.redis.set(self._key(session_id), str(user_id), ex=ttl)
        )


    async def get_user(self, session_id: UUID) -> UUID | None:

        value = await self.redis.get(self._key(session_id))

        if value is None:
            return None

        if isinstance(value, bytes):
            value = value.decode()

        return UUID(value)


    async def revoke(self, session_id: UUID) -> bool:

        return bool(
            await self.redis.delete(self._key(session_id))
        )


class RateLimiter:

    def __init__(self, client: RedisClient) -> None:

        self.redis = client.client


    def _key(self, identifier: str, endpoint: str) -> str:

        return f"rate:{endpoint}:{identifier}"


    async def increment(self, identifier: str, endpoint: str, *, window: int) -> int:

        key = self._key(identifier, endpoint)

        count = await self.redis.incr(key)

        if count == 1:
            await self.redis.expire(key, window)

        return count


    async def allowed(self, identifier: str, endpoint: str, *, limit: int, window: int) -> bool:

        count = await self.increment(identifier, endpoint, window=window)

        return count <= limit


class APICache:

    def __init__(self, client: RedisClient) -> None:

        self.redis = client.client


    def _key(self, namespace: str, key: str) -> str:

        return f"cache:{namespace}:{key}"


    async def get(self, namespace: str, key: str) -> str | None:

        return cast(str | None, await self.redis.get(self._key(namespace, key)))


    async def set(self, namespace: str, key: str, value: str, *, ttl: int) -> bool:
        return bool(
            await self.redis.set(self._key(namespace, key), value, ex=ttl)
        )


    async def invalidate(self, namespace: str, key: str) -> bool:
        return bool(
            await self.redis.delete(self._key(namespace, key))
        )


class TaskProgress:

    def __init__(self, client: RedisClient) -> None:

        self.redis = client.client


    def _key(self, task_id: UUID) -> str:

        return f"task:progress:{task_id}"


    async def set(self, task_id: UUID, progress: str, *, ttl: int = 3600) -> bool:
        return bool(
            await self.redis.set(self._key(task_id), progress, ex=ttl)
        )


    async def get(self, task_id: UUID) -> str | None:

        return cast(str | None, await self.redis.get(self._key(task_id)))


    async def delete(self, task_id: UUID) -> bool:
        return bool(
            await self.redis.delete(self._key(task_id))
        )