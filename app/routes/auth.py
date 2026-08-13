from fastapi import APIRouter

from app.models import LoginRequest, LoginResponse


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    print(request.email)
    print(request.password)

    return LoginResponse(
        access_token="jwt-token",
        token_type="bearer"
    )