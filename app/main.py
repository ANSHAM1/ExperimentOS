from fastapi import FastAPI

from app.routes import auth_router

from app.core import get_settings
from app.db import get_db_session, Postgres
from app.schemas import User


db_session = get_db_session(Postgres(get_settings().POSTGRES_URL))
users = User()



app = FastAPI(
    title="ExperimentOS",
    version="0.1.0",
)


app.include_router(auth_router)


@app.get("/health")
async def health():
    return {"status": "ok"}