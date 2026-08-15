from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker, create_async_engine)



class PostgresDatabase:

    def __init__(self, database_url: str) -> None:

        engine = create_async_engine(
            database_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=1800,
        )

        self.session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )