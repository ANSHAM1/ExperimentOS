from typing import Any

from datetime import datetime, timedelta, timezone
from uuid import UUID

import secrets
import hashlib
import jwt

from app.core import get_settings
settings = get_settings()



class TokenUtility:

    def __init__(self) -> None:

        self.secret_key: str = settings.JWT_SECRET_KEY
        
        self.algorithm: str = settings.JWT_ALGORITHM

        self.access_token_expire_minutes: int = (settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

        self.issuer: str = settings.JWT_ISSUER

        self.audience: str = settings.JWT_AUDIENCE


    def create_refresh_token(self) -> str:
        return secrets.token_urlsafe(64)


    def hash_refresh_token(self, refresh_token: str) -> str:
        return hashlib.sha256(refresh_token.encode()).hexdigest()


    def create_access_token(self, user_id: UUID, session_id: UUID, role: str) -> str:

        now = datetime.now(timezone.utc)

        expires_at = now + timedelta(minutes=self.access_token_expire_minutes)

        payload: dict[str, Any] = {
            "sub": str(user_id),
            "sid": str(session_id),
            "role": role,
            "iat": now,
            "exp": expires_at,
            "iss": self.issuer,
            "aud": self.audience,
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm) # type: ignore


    def decode_access_token(self, token: str) -> dict[str, Any]:

        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm], issuer=self.issuer, audience=self.audience, # type: ignore
            options={
                "require": ["sub", "sid", "role", "iat", "exp", "iss", "aud"]
            }
        )