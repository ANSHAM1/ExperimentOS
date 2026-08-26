from pydantic import BaseModel, EmailStr

from app.models import Role



class RegisterData(BaseModel):
    user_id: str
    email: EmailStr
    role: Role


class RegisterRequest(BaseModel):
    email : EmailStr
    password : str


class RegisterResponse(BaseModel):
    success: bool
    message: str
    data: RegisterData | None = None



class EmailVerificationRequest(BaseModel):
    email: EmailStr
    otp: str


class EmailVerificationResponse(BaseModel):
    success: bool
    message: str



class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str