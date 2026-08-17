from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes import auth_router
from app.core import get_settings

from app.db import Postgres
from app import schemas as _



postgres = Postgres(get_settings().POSTGRES_URL)

@asynccontextmanager
async def lifespan(_: FastAPI):

    await postgres.init_db()

    yield

    await postgres.close()


app = FastAPI(
    title="ExperimentOS",
    lifespan=lifespan,
)


app.include_router(auth_router)


@app.get("/")
async def health():
    return {"status": "ok"}