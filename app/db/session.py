from typing import Protocol

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker)



class Database(Protocol):

    session_factory : async_sessionmaker[AsyncSession]



async def get_db_session(database: Database) -> AsyncGenerator[AsyncSession, None]:

    async with database.session_factory() as session:
        yield session