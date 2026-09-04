from abc import ABC



class AgentDispatch(ABC):

    @staticmethod
    async def run(payload: dict[str, object]) -> None:

        raise NotImplementedError("Must implement the run method.")