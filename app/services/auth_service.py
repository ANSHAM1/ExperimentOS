from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.redis import SessionStore
from app.repository import UserRepository

from app.models import User
from app.schemas import LoginRequest, RegisterRequest, RegisterResponse, RegisterData

from .password_service import PasswordService
# from .token_service import TokenService

# from app.core import get_settings




class AuthService:

    def __init__(self, db_session: AsyncSession, session_store: SessionStore) -> None:

        self.db_session    = db_session

        self.session_store = session_store


    async def Login(self, req: LoginRequest) -> None:

        pass


    async def Register(self, req: RegisterRequest) -> RegisterResponse:

        email = req.email.strip().lower()

        try:
            
            user_repo = UserRepository(self.db_session)

            if await user_repo.exists_by_email(email):
                return RegisterResponse(
                    success=False,
                    message="Email ID already exists",
                    data=None,
                )

            user = await user_repo.create(
                User(
                    email=email,
                    password_hash=PasswordService.hash(req.password)
                )
            )

            await user_repo.commit()

            return RegisterResponse(
                    success=True,
                    message="User Registered Successfully",
                    data=RegisterData(
                        user_id=str(user.id),
                        email=user.email,
                        role=user.role,
                    ),
                )

        except IntegrityError:

            await self.db_session.rollback()

            return RegisterResponse(
                success=False,
                message="Email ID already exists",
                data=None,
            )