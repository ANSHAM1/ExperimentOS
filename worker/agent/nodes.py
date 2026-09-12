from typing import Any

from worker.llm import LLM_Factory
from worker.runner import Python
from worker.schema import CodeGenOutput, CodeExeOutput, CodeEvalOutput
from worker.prompt import code_generation_prompt, code_evaluation_prompt, code_retry_prompt

from .state import ExperimentState

from app.core import get_settings
settings = get_settings()



def generation_prompt_node(state: ExperimentState) -> dict[str, Any]:

    prompt = code_generation_prompt.invoke(
        {
            "human_prompt": state["human_prompt"],
        }
    )

    return {
        "prompt": prompt
    }



def retry_prompt_node(state: ExperimentState) -> dict[str, Any]:

    if state["output_code"] is None or state["output_exec"] is None:
        raise RuntimeError(
            f"Missing retry context for experiment "
            f"{state['experiment_id']}"
        )

    prompt = code_retry_prompt.invoke(
        {
            "human_prompt": state["human_prompt"],
            "generated_code": state["output_code"].code,
            "execution_result": state["output_exec"].model_dump(),
        }
    )

    return {
        "prompt": prompt
    }



def evaluation_prompt_node(state: ExperimentState) -> dict[str, Any]:

    if state["output_code"] is None or state["output_exec"] is None:
        raise RuntimeError(
            f"Missing evaluation context for experiment "
            f"{state['experiment_id']}"
        )

    prompt = code_evaluation_prompt.invoke(
        {
            "human_prompt": state["human_prompt"],
            "generated_code": state["output_code"].code,
            "execution_result": state["output_exec"].model_dump(),
        }
    )

    return {
        "prompt": prompt
    }



async def code_generation_node(state: ExperimentState) -> dict[str, Any]:

    try:
        response = await LLM_Factory.OpenAI_StrucutredOutput(
            input=state["prompt"], schema=CodeGenOutput, model=settings.SELECTED_MODEL, temperature=0.2, reasoning=False
            )

    except Exception as exc:
        raise RuntimeError("Code Generation Node - LLM Response Failure") from exc

    return {
        "output_code": response
    }



async def code_evaluation_node(state: ExperimentState) -> dict[str, Any]:

    try:
        response = await LLM_Factory.OpenAI_StrucutredOutput(
            input=state["prompt"], schema=CodeEvalOutput, model=settings.SELECTED_MODEL, temperature=0.2, reasoning=True
            )

    except Exception as exc:
        raise RuntimeError("Code Evaluation Node - LLM Response Failure") from exc

    return {
        "output_eval": response
    }



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
        raise RuntimeError("Code Execution Node - Execution Failure") from exc

    execution_result = CodeExeOutput(
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
        timed_out=returncode == -1,
    )

    return {
        "output_exec" : execution_result
    }



def execution_router(state: ExperimentState) -> str:

    if state["terminate"]:
        return "terminate"

    if state["retry"]:
        return "retry"

    return "evaluate"   



def retry_node(state: ExperimentState) -> dict[str, Any]:

    output_exec = state["output_exec"]

    if output_exec is None:
        raise RuntimeError("Retry Node - Missing execution output")

    if output_exec.returncode == 0:
        return {
            "retry": False,
            "terminate": False,
        }

    retry_count = state["retry_count"] + 1

    if retry_count > settings.RETRY_COUNT:
        return {
            "retry_count": retry_count,
            "retry": False,
            "terminate": True,
        }

    return {
        "retry_count": retry_count,
        "retry": True,
        "terminate": False,
    }