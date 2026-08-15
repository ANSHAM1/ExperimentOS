from fastapi import FastAPI

from app.routes import auth_router

from app.core import get_settings
from app.db import get_db_session, PostgresDatabase


db_session = get_db_session(PostgresDatabase(get_settings().POSTGRES_URL))

app = FastAPI(
    title="ExperimentOS",
    version="0.1.0",
)


app.include_router(auth_router)


@app.get("/health")
async def health():
    return {"status": "ok"}