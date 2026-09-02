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


    async def get_session(self, session_id: UUID) -> tuple[UUID, str] | None:

        value = await self.redis.get(self._key(session_id))

        if value is None:
            return None

        if isinstance(value, bytes):
            value = value.decode()

        user_id, refresh_token_hash = value.split(":", 1)

        return UUID(user_id), refresh_token_hash


    async def rotate_session(self, old_session_id: UUID, presented_refresh_token_hash: str,
        new_session_id: UUID, new_refresh_token_hash: str, ttl: int) -> UUID | None:

        script = """
        local old_key = KEYS[1]
        local new_key = KEYS[2]

        local stored = redis.call("GET", old_key)

        if not stored then
            return nil
        end

        local separator = string.find(stored, ":")

        if not separator then
            return nil
        end

        local user_id = string.sub(
            stored,
            1,
            separator - 1
        )

        local stored_hash = string.sub(
            stored,
            separator + 1
        )

        if stored_hash ~= ARGV[1] then
            return nil
        end

        redis.call(
            "SET",
            new_key,
            user_id .. ":" .. ARGV[2],
            "EX",
            ARGV[3]
        )

        redis.call("DEL", old_key)

        return user_id
        """

        result = await self.redis.eval(
            script,
            2,
            self._key(old_session_id),
            self._key(new_session_id),
            presented_refresh_token_hash,
            new_refresh_token_hash,
            ttl,
        )

        if result is None:
            return None

        return UUID(result)


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