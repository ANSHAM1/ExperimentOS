from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes import auth_router
from app.core import redis, postgres

from app import models as _



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