from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class PublishCommentRequest(BaseModel):
    lead_id: UUID
    comment: str
    reddit_username: str
    reddit_password: str


class PublishCommentDataObject(BaseModel):
    url: str
    body: str
    title: str


class PublishCommentResponse(BaseModel):
    id: UUID
    discovered_at: datetime
    last_contacted_at: datetime | None = None
    reddit_id: str | None = None
    prospect_username: str
    prospect_name: str | None = None
    source: str
    data: PublishCommentDataObject | None = None
    last_event: str
    status: str
    comment: str | None = None

