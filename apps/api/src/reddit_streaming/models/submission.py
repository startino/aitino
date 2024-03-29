from pydantic import BaseModel

class Submission(BaseModel):
    id: str
    author:str = "r/antopia_hk"
    title: str
    selftext: str
    created_utc: float
    url: str

