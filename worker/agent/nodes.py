from typing import Any

from worker.llm import LLM_Factory
from worker.runner import Python
from worker.schema import Step, CodeGenOutput, CodeExeOutput, CodeEvalOutput
from worker.prompt import code_generation_prompt, code_evaluation_prompt, code_retry_prompt

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



async def code_generation_node(state: ExperimentState) -> dict[str, Any]:

    match state["step"]:

        case Step.GENERATION | Step.RETRY:
            response = await LLM_Factory.OpenAI_StrucutredOutput(
                input=state["prompt"], schema=CodeGenOutput, model=settings.SELECTED_MODEL, temperature=0.2, reasoning=False
                )

            return { 
                "output_code" : response,
                "terminate" : False
                }

        case Step.EVALUATION:
            response = await LLM_Factory.OpenAI_StrucutredOutput(
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



async def code_execution_node(state: ExperimentState) -> dict[str, Any]:

    output_code = state["output_code"]

    if output_code is None:
        raise RuntimeError(
            f"Missing generated code for experiment "
            f"{state['experiment_id']}"
        )

    timeout = min(output_code.ttl, settings.MAX_EXECUTION_TIMEOUT)

    try:
        returncode, stdout, stderr = await Python.execute(state["experiment_id"], output_code.code, timeout)

    except Exception as exc:
        raise RuntimeError(
            f"Experiment execution failed unexpectedly: "
            f"{state['experiment_id']}"
        ) from exc

    return {
        "output_exec": CodeExeOutput(
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
            timed_out=returncode == -1,
        )
    }