from app.redis import SessionStore
from app.repository import UserRepository
# from app.models import User

# from .password_service import PasswordService
# from .token_service import TokenService

# from app.core import get_settings


class AuthService:

    def __init__(self, user_repo: UserRepository, session_store: SessionStore) -> None:

        self.user_repo     = user_repo

        self.session_store = session_store



    async def Login(self, email: str, password: str) -> None:

        pass


    async def Register(self, UserRepo: UserRepository) -> None:

        pass