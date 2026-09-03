from typing import Any

from fastapi import APIRouter, Depends

from app.schemas import ExperimentRequest, ExperimentResponse
from app.dependency import AuthDependency



agent_router = APIRouter(
    prefix="/agent",
    tags=["AI Agent Workflow"]
)



@agent_router.post("/experiment", response_model=ExperimentResponse)
async def agent(req: ExperimentRequest, auth: dict[str, Any] = Depends(AuthDependency.get_auth)):

    return ExperimentResponse(output=f"This is a sample response from the AI agent. You said: {req}")