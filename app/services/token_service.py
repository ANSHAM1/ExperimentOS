from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID

import jwt



class TokenService:

    def __init__(self, secret_key: str, algorithm: str = "", access_token_expire_minutes: int = 30, 
                 issuer: str = "experimentos", audience: str = "experimentos-api") -> None:
        
        self.secret_key = secret_key

        self.algorithm = algorithm

        self.access_token_expire_minutes = access_token_expire_minutes

        self.issuer = issuer

        self.audience = audience


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
                "require": ["sub", "sid", "role", "iat", "exp", "iss", "aud",]
            }
        )