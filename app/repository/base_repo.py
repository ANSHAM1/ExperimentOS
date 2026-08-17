from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base



class BaseRepository:

    def __init__(self, session: AsyncSession) -> None:

        self.session = session


    async def __aenter__(self) -> Self:

        return self


    async def __aexit__(self, exc_type: type[BaseException] | None, _1: BaseException | None, _2: TracebackType | None) -> bool:

        if exc_type is not None:
            await self.session.rollback()

        return False


    def add(self, entity: Base) -> None:

        self.session.add(entity)


    def add_all(self, entities: list[Base]) -> None:

        self.session.add_all(entities)


    async def delete(self, entity: Base) -> None:

        await self.session.delete(entity)


    async def flush(self) -> None:

        await self.session.flush()


    async def refresh(self, entity: Base) -> None:

        await self.session.refresh(entity)


    async def commit(self) -> None:

        await self.session.commit()


    async def rollback(self) -> None:

        await self.session.rollback()