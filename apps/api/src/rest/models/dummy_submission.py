from pydantic import BaseModel, Field

class DummySubmission(BaseModel):
    id: str
    url: str
    created_utc: int
    title: str
    selftext: str