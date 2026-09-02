from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import LoginRequest, RefreshRequest, TokenResponse, RegisterRequest, RegisterResponse, EmailVerificationRequest, EmailVerificationResponse
from app.services import AuthService
from app.core import redis, get_postgres_session


DBSession = Annotated[AsyncSession, Depends(get_postgres_session)]


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@auth_router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db_session: DBSession):

    return await AuthService(db_session, redis).Login(request)


@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh(request: RefreshRequest, db_session: DBSession):

    return await AuthService(db_session, redis).refresh(request)



@auth_router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, db_session: DBSession):

    return await AuthService(db_session, redis).Register(request)



@auth_router.post("/verify", response_model=EmailVerificationResponse)
async def verify_email(request: EmailVerificationRequest, db_session: DBSession):

    return await AuthService(db_session, redis).VerifyEmail(request)