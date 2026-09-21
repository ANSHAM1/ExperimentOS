from uuid import uuid4

from worker.schema import AgentPayload

from worker.agent import ExperimentState, AgentGraph



class AgentDispatch:

    @staticmethod
    async def run(payload: AgentPayload) -> None:

        state: ExperimentState = {
            "experiment_id": str(uuid4()),
            "user_id": payload["user_id"],

            "retry_count": 0,

            "prompt": None,
            "human_prompt": payload["message"],

            "output_code": None,
            "output_exec": None,
            "output_eval": None,

            "terminate": False,
            "retry": False,
        }

        await AgentGraph.ainvoke(state) # type: ignore[arg-type]