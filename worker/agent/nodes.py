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
                    "execution_result": state["output_exec"].model_dump(),
                }
            )

        case _:
            raise ValueError(f"Unsupported experiment step: {state['step']}")

    return { "prompt": prompt }



async def code_generation_node(state: ExperimentState) -> dict[str, Any]:

    match state["step"]:

        case Step.GENERATION | Step.RETRY:
            try:
                response = await LLM_Factory.OpenAI_StrucutredOutput(
                    input=state["prompt"], schema=CodeGenOutput, model=settings.SELECTED_MODEL, temperature=0.2, reasoning=False
                    )

            except Exception:
                return {
                    "terminate": True,
                }

            return {
                "output_code": response,
                "terminate": False,
            }

        case Step.EVALUATION:
            try:
                response = await LLM_Factory.OpenAI_StrucutredOutput(
                    input=state["prompt"], schema=CodeEvalOutput, model=settings.SELECTED_MODEL, temperature=0.2, reasoning=False
                    )

            except Exception:
                return {
                    "terminate": True,
                }

            return {
                "output_eval": response,
                "terminate": False,
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

    except Exception:
        if state["retry_count"] < settings.RETRY_COUNT:
            return {
                "retry": True,
            }

        return {
            "terminate": True,
        }

    execution_result = CodeExeOutput(
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
        timed_out=returncode == -1,
    )

    if returncode != 0:
        return {
            "output_exec": execution_result,
            "retry": state["retry_count"] < settings.RETRY_COUNT,
            "terminate": state["retry_count"] >= settings.RETRY_COUNT,
        }

    return {
        "output_exec": execution_result,
        "retry": False,
        "terminate": False,
    }



def retry_router(state: ExperimentState) -> str:

    if state["retry"]:
        return "yes"

    return "no"



def increment_retry_node(state: ExperimentState) -> dict[str, Any]:

    return {
        "retry_count": state["retry_count"] + 1,
        "step": Step.RETRY,
    }