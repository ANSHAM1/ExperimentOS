from pydantic import BaseModel, Field



class ExecuteRequest(BaseModel):
    experiment_id: str
    code: str = Field(min_length=1)


class ExecuteResponse(BaseModel):
    experiment_id: str
    success: bool
    exit_code: int
    stdout: str
    stderr: str