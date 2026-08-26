from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, EmailVerificationRequest, EmailVerificationResponse
from app.services import AuthService
from app.core import redis, get_postgres_session


DBSession = Annotated[AsyncSession, Depends(get_postgres_session)]


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db_session: DBSession):

    return LoginResponse(
        access_token="jwt-token",
        token_type="bearer"
    )



@auth_router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, db_session: DBSession):

    return await AuthService(db_session, redis).Register(request)



@auth_router.post("/verify", response_model=EmailVerificationResponse)
async def email_verify(request: EmailVerificationRequest, db_session: DBSession):

    return await AuthService(db_session, redis).EmailVerification(request)