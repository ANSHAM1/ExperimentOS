from uuid import UUID

from sqlalchemy import select, update

from app.models import User

from .base_repo import BaseRepository



class UserRepository(BaseRepository):

    async def get_by_id(self, user_id: UUID) -> User | None:

        return (await self.session.execute(select(User).where(User.id == user_id))).scalar_one_or_none()


    async def get_by_email(self, email: str) -> User | None:

        return (await self.session.execute(select(User).where(User.email == email))).scalar_one_or_none()


    async def exists_by_email(self, email: str) -> bool:

        return (await self.session.execute(select(User.is_active).where(User.email == email))).scalar_one_or_none() is not None


    async def set_user_active_state_to(self, email:str, state: bool) -> None:

        await self.session.execute(update(User).where(User.email == email).values(is_active=state))


    async def create(self, user: User) -> User:

        self.add(user)

        await self.flush()
        await self.refresh(user)

        return user