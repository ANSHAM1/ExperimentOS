from typing import Any

from app.redis import RedisClient, SessionStore, RateLimiter

from app.services import TokenUtility



class AuthDependency:

    @staticmethod
    async def get_auth(redis_client: RedisClient, token: str) -> dict[str, Any]:

        auth = TokenUtility().decode_access_token(token)

        session_data = await SessionStore(redis_client).get_session(auth["sid"])

        if session_data is None:
            return {
                "message": "Session not found",
                "status_code": 401
            }

        return auth    