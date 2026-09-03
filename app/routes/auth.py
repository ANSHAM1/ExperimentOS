from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Response, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import LoginRequest, RefreshRequest, TokenResponse, RegisterRequest, RegisterResponse, EmailVerificationRequest, EmailVerificationResponse
from app.services import AuthService
from app.core import redis, get_postgres_session, get_settings

settings = get_settings()


DBSession = Annotated[AsyncSession, Depends(get_postgres_session)]


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@auth_router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, response: Response, db_session: DBSession):

    return await AuthService(db_session, redis).Login(request, response)



@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh(response: Response, db_session: DBSession, refresh_token: str | None = Cookie(default=None), session_id: str | None = Cookie(default=None)):

    if refresh_token is None or session_id is None:
        return TokenResponse(
            success=False,
            message="Invalid refresh token or session ID",
            access_token=None,
            token_type=None,
        )

    request = RefreshRequest(
        session_id=UUID(session_id),
        refresh_token=refresh_token
    )

    return await AuthService(db_session, redis).refresh(request, response)



@auth_router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, db_session: DBSession):

    return await AuthService(db_session, redis).Register(request)



@auth_router.post("/verify", response_model=EmailVerificationResponse)
async def verify_email(request: EmailVerificationRequest, db_session: DBSession):

    return await AuthService(db_session, redis).VerifyEmail(request)