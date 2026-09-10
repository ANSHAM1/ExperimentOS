from typing import Any

from worker.llm import LLM_Factory
from worker.prompt import code_generation_prompt, code_evaluation_prompt, code_retry_prompt
from worker.schema import Step

from .state import ExperimentState



def prompt_builder_node(state: ExperimentState) -> dict[str, Any]:

    match state["step"]:

        case Step.GENERATION:
            prompt = code_generation_prompt.invoke(
                {
                    "human_prompt": state["human_prompt"],
                }
            )

        case Step.EVALUATION | Step.RETRY:
            prompt_template = {
                Step.EVALUATION: code_evaluation_prompt,
                Step.RETRY: code_retry_prompt,
            }[state["step"]]

            prompt = prompt_template.invoke(
                {
                    "human_prompt": state["human_prompt"],
                    "generated_code": state["generated_code"],
                    "execution_result": state["execution_result"],
                }
            )

        case _:
            raise ValueError(
                f"Unsupported experiment step: {state['step']}"
            )

    return {"prompt": prompt}



def code_generation_node(state: ExperimentState) -> dict[str, Any]:

    response = LLM_Factory.OpenAI_StrucutredOutput(input=state["prompt"], schema="", model="", temperature=0.2, reasoning=False)

    if response is None:
        return {
            "terminate": True,
        }

    return {
        "metadata": response,
        "terminate": False,
    }



def terminate_router(state: ExperimentState) -> str:

    if state["terminate"]:
        return "yes"

    return "no"