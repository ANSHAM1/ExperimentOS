from uuid import UUID

from app.redis import RedisClient


class SessionStore:

    def __init__(self, client: RedisClient) -> None:

        self.redis = client.client


    def _key(self, session_id: UUID) -> str:

        return f"auth:session:{session_id}"


    async def create_session(self, session_id: UUID, user_id: UUID, *, refresh_token_hash: str, ttl: int) -> bool:

        return bool(
            await self.redis.set(self._key(session_id), f"{user_id}:{refresh_token_hash}", ex=ttl)
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


class OtpValidator:

    def __init__(self, client: RedisClient) -> None:

        self.redis = client.client


    def _key(self, email: str) -> str:

        return f"otp:{email}"


    async def store_otp(self, email: str, otp: str, *, window: int) -> None:

        key = self._key(email)

        await self.redis.set(key, otp, ex=window)


    async def validate_otp(self, email: str, otp: str) -> bool:

        key = self._key(email)

        stored_otp = await self.redis.get(key)

        if stored_otp is None:
            return False

        if stored_otp != otp:
            return False

        await self.redis.delete(key)

        return True