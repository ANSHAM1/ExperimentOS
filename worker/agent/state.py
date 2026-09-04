from typing import Any, TypedDict


class ExperimentState(TypedDict, total=False):

    experiment_id    : str
    user_id          : str
    prompt           : str

    models           : list[dict[str, Any]]
    dataset          : dict[str, Any]
    metrics          : list[str]

    generated_code   : str
    execution_result : dict[str, Any]

    model_results    : list[dict[str, Any]]
    comparison       : dict[str, Any]

    error            : str | None