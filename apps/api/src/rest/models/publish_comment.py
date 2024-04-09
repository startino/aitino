from uuid import UUID
from pydantic import BaseModel

class PublishCommentRequest(BaseModel):
    lead_id: UUID
    comment: str
    reddit_username: str
    reddit_password: str

