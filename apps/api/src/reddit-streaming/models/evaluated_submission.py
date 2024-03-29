from pydantic import BaseModel

class EvaluatedSubmission(BaseModel):
    is_relevant: bool
    cost: float
    reason: str