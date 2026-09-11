from typing import Any, Literal

from pydantic import BaseModel, Field



class CodeGenOutput(BaseModel):
    code: str = Field(min_length=1)
    ttl: int = Field(gt=0, le=1800, description="Execution timeout in seconds")



class CodeEvalOutput(BaseModel):
    experiment_type: Literal["training", "comparison"]
    results: dict[str, Any]
    best_model: str | None = None
    comparison: dict[str, Any] | None = None
    summary: str