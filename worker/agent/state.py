from typing import TypedDict

from langchain_core.prompt_values import PromptValue

from worker.schema import Step, CodeGenOutput, CodeEvalOutput


class ExperimentState(TypedDict):

    experiment_id    : str
    user_id          : str

    step             : Step
    prompt           : PromptValue
    human_prompt     : str

    output_code      : CodeGenOutput | None 
    output_exec      : str | None

    output_eval      : CodeEvalOutput

    terminate        : bool