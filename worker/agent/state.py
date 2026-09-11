from typing import TypedDict

from langchain_core.prompt_values import PromptValue

from worker.schema import Step, CodeGenOutput, CodeExeOutput, CodeEvalOutput


class ExperimentState(TypedDict):

    experiment_id    : str
    user_id          : str

    retry_count      : int

    step             : Step
    prompt           : PromptValue
    human_prompt     : str

    output_code      : CodeGenOutput | None 
    output_exec      : CodeExeOutput | None

    output_eval      : CodeEvalOutput

    terminate        : bool
    retry            : bool