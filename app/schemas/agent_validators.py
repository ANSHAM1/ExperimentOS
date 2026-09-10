from pydantic import BaseModel



class ExperimentRequest(BaseModel):
    prompt: str


class ExperimentResponse(BaseModel):
    output: str 