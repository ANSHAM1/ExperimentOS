from fastapi import APIRouter, Depends

from app.schemas import AgentRequest, AgentResponse
from app.dependency import AuthDependency



agent_router = APIRouter(
    prefix="/agent",
    tags=["AI Agent Workflow"]
)



@agent_router.post("/agent", response_model=AgentResponse)
async def agent(req: AgentRequest, auth: AuthDependency = Depends(AuthDependency.get_auth)):

    return AgentResponse(output=f"This is a sample response from the AI agent. You said: {req.prompt}")