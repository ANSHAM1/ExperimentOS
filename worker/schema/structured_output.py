from pydantic import BaseModel, Field



class CodeGenOutput(BaseModel):
    code: str = Field(min_length=1)
    ttl: str = Field(description="Provide ttl in seconds")



class CodeExeOutput(BaseModel):
    output: str 