from typing import TypedDict


class AgentPayload(TypedDict):
    user_id: str
    message: str