from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Session(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    maeve_id: UUID
    profile_id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
