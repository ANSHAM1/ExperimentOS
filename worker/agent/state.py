from typing import Any, TypedDict

from worker.schema import Step, CodeGenOutput, CodeExeOutput


class ExperimentState(TypedDict):

    experiment_id    : str
    user_id          : str

    step             : Step
    prompt           : str
    human_prompt     : str

    output_code      : CodeGenOutput
    output_exec      : CodeExeOutput

    model_results    : list[dict[str, Any]]
    comparison       : dict[str, Any]

    terminate        : bool