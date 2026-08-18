from uuid import UUID

from .base_cache import BaseCache



class UserCache(BaseCache):

    def _user_key(self, user_id: UUID) -> str:

        return f"user:{user_id}"


    def _email_key(self, email: str) -> str:

        return f"user:email:{email}"


    async def set_user(self, user_id: UUID, data: str, *, ex: int | None = None) -> bool:

        return await self.set(self._user_key(user_id), data, ex=ex)


    async def get_user(self, user_id: UUID) -> str | None:

        return await self.get(self._user_key(user_id))


    async def delete_user(self, user_id: UUID) -> int:

        return await self.delete(self._user_key(user_id))


    async def set_user_by_email(self, email: str, data: str, *, ex: int | None = None) -> bool:

        return await self.set(self._email_key(email), data, ex=ex)


    async def get_user_by_email(self, email: str) -> str | None:

        return await self.get(self._email_key(email))


    async def delete_user_by_email(self, email: str) -> int:

        return await self.delete(self._email_key(email))