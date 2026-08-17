from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes import auth_router
from app.core import get_settings

from app.db import Postgres, RedisClient
from app import models as _



postgres = Postgres(get_settings().POSTGRES_URL)
redis = RedisClient(get_settings().REDIS_URL)

@asynccontextmanager
async def lifespan(_: FastAPI):

    await postgres.init_db()

    if not await redis.ping():
        raise RuntimeError("Redis connection failed")

    yield

    await postgres.close()

    await redis.close()


app = FastAPI(
    title="ExperimentOS",
    lifespan=lifespan,
)


app.include_router(auth_router)


@app.get("/")
async def health():
    return {"status": "ok"}