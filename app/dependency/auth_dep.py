from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from app.redis import RedisClient, SessionStore
from app.services import TokenUtility

from app.core import redis


bearer = HTTPBearer()


class AuthDependency:

    @staticmethod
    async def get_auth(
        credentials: HTTPAuthorizationCredentials = Depends(bearer), 
        redis_client: RedisClient = Depends(lambda: redis)
    ) -> dict[str, Any]:

        try:

            auth = TokenUtility().decode_access_token(credentials.credentials)

        except InvalidTokenError:
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired access token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        session_data = await SessionStore(redis_client).get_session(auth["sid"])

        if session_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired or revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return auth