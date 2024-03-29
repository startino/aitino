from pydantic import BaseModel

class Submission(BaseModel):
    id: str
    title: str
    selftext: str
    created_utc: float
    url: str

