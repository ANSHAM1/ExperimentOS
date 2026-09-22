from typing import Literal

from pydantic import BaseModel, Field



class CodeGenOutput(BaseModel):
    code: str = Field(min_length=1)
    ttl: int = Field(gt=0, le=1800, description="Execution timeout in seconds")



class CodeExeOutput(BaseModel):
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False



class CodeEvalOutput(BaseModel):
    experiment_type: Literal["training", "comparison"]
    success: bool
    results: str
    artifacts: list[str] = Field(default_factory=list)
    best_model: str | None = None
    comparison: str | None = None
    summary: str
    errors: list[str] = Field(default_factory=list)