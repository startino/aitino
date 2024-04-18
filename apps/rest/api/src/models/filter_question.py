from pydantic import BaseModel

class FilterQuestion(BaseModel):
    question: str
    reject_on: bool

