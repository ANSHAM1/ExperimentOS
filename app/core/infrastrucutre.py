from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

from app.core import get_settings
from app.db import Postgres, get_db_session
from app.redis import RedisClient



settings = get_settings()


postgres = Postgres(settings.POSTGRES_URL)
redis = RedisClient(settings.REDIS_URL)


async def get_postgres_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_session(postgres):
        yield session