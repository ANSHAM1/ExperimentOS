from worker.schema import AgentPayload

from worker.agent import ExperimentState, AgentGraph



class AgentDispatch:

    @staticmethod
    async def run(payload: AgentPayload) -> None:

        state: ExperimentState = {
            "experiment_id": payload["experiment_id"],
            "user_id": payload["user_id"],

            "retry_count": 0,

            "prompt": None,
            "human_prompt": payload["user_prompt"],

            "output_code": None,
            "output_exec": None,
            "output_eval": None,

            "terminate": False,
            "retry": False,
        }

        await AgentGraph.ainvoke(state) # type: ignore[arg-type]