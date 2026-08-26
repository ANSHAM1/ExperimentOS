from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from app.services import AuthService
from app.core import redis, get_postgres_session


DBSession = Annotated[AsyncSession, Depends(get_postgres_session)]


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)



@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):

    return LoginResponse(
        access_token="jwt-token",
        token_type="bearer"
    )



@auth_router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, db_session: DBSession):

    await AuthService(db_session, redis).Register(request)