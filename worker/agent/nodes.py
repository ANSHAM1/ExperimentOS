from typing import Any

from worker.llm import LLM_Factory
from worker.prompt import code_generation_prompt, code_evaluation_prompt, code_retry_prompt
from worker.schema import Step, CodeGenOutput, CodeEvalOutput

from .state import ExperimentState

from app.core import get_settings
settings = get_settings()



def prompt_builder_node(state: ExperimentState) -> dict[str, Any]:

    match state["step"]:

        case Step.GENERATION:
            prompt = code_generation_prompt.invoke(
                {
                    "human_prompt": state["human_prompt"],
                }
            )

        case Step.EVALUATION | Step.RETRY:

            if state["output_code"] is None or state["output_exec"] is None:
                raise ValueError("Enternal Server Error - Agent Node")
    
            prompt_template = {
                Step.EVALUATION: code_evaluation_prompt,
                Step.RETRY: code_retry_prompt,
            }[state["step"]]

            prompt = prompt_template.invoke(
                {
                    "human_prompt": state["human_prompt"],
                    "generated_code": state["output_code"].code,
                    "execution_result": state["output_exec"],
                }
            )

        case _:
            raise ValueError(f"Unsupported experiment step: {state['step']}")

    return { "prompt": prompt }



def code_generation_node(state: ExperimentState) -> dict[str, Any]:

    match state["step"]:

        case Step.GENERATION | Step.RETRY:
            response = LLM_Factory.OpenAI_StrucutredOutput(
                input=state["prompt"], schema=CodeGenOutput, model=settings.SELECTED_MODEL, temperature=0.2, reasoning=False
                )

            return { 
                "output_code" : response,
                "terminate" : False
                }

        case Step.EVALUATION:
            response = LLM_Factory.OpenAI_StrucutredOutput(
                input=state["prompt"], schema=CodeEvalOutput, model=settings.SELECTED_MODEL, temperature=0.2, reasoning=False
                )

            return { 
                "output_exec" : response,
                "terminate" : False
                }

        case _:
            return {
                "terminate" : True
                }



def terminate_router(state: ExperimentState) -> str:

    if state["terminate"]:
        return "yes"

    return "no"



def code_execution_node(state: ExperimentState) -> dict[str, Any]:

    return {}