from typing import Any, TypedDict

from worker.schema import Step


class ExperimentState(TypedDict):

    experiment_id    : str
    user_id          : str

    step             : Step
    prompt           : str
    human_prompt     : str

    generated_code   : str
    execution_result : dict[str, Any]

    model_results    : list[dict[str, Any]]
    comparison       : dict[str, Any]

    terminate        : bool