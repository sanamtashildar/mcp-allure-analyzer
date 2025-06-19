from pydantic import BaseModel

class Failure(BaseModel):
    name: str
    message: str
    reason: str
