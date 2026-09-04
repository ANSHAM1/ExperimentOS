from typing import Any

from fastapi import APIRouter, Depends

from app.schemas import ExperimentRequest, ExperimentResponse
from app.dependency import AuthDependency

from app.rabbitmq import RabbitMQRepository
from app.core import rabbitmq, get_settings

settings = get_settings()


agent_router = APIRouter(
    prefix="/agent",
    tags=["AI Agent Workflow"]
)



@agent_router.post("/experiment", response_model=ExperimentResponse)
async def agent(req: ExperimentRequest, auth: dict[str, Any] = Depends(AuthDependency.get_auth)):

    payload: dict[str, object] = {
        "user_id": auth["sub"],
        "message": req.model_dump(mode="json"),
    }

    await RabbitMQRepository(rabbitmq.channel).publish(settings.EXPERIMENT_QUEUE, payload)