from typing import TypedDict


class AgentPayload(TypedDict):
    experiment_id: str
    user_id: str
    user_prompt: str