from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes import auth_router, agent_router
from app.core import redis, postgres, rabbitmq
from app.rabbitmq import RabbitMQRepository

from app import models as _

from app.core import get_settings
settings = get_settings()



@asynccontextmanager
async def lifespan(_: FastAPI):
    await postgres.init_db()

    if not await redis.ping():
        raise RuntimeError("Redis connection failed")

    await rabbitmq.connect()
    await RabbitMQRepository(rabbitmq.channel).declare_queue(settings.EXPERIMENT_QUEUE, durable=True)

    yield

    await rabbitmq.close()
    await postgres.close()
    await redis.close()


app = FastAPI(
    title="ExperimentOS",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)


app.include_router(auth_router)
app.include_router(agent_router)


@app.get("/")
async def health():
    return {"status": "ok"}