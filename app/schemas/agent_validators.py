from uuid import UUID

from pydantic import BaseModel



class ModelSpec(BaseModel):
    name: str

class DatasetSpec(BaseModel):
    source: str
    name: str

class EvaluationSpec(BaseModel):
    metrics: list[str]

class ExperimentRequest(BaseModel):
    experiment_id: UUID
    prompt: str
    models: list[ModelSpec]
    dataset: DatasetSpec
    evaluation: EvaluationSpec


class ExperimentResponse(BaseModel):
    output: str 