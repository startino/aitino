from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from datetime import datetime

# = Field(default_factory=lambda: uuid4())

class Profile(BaseModel):
    id: UUID
    tier_id: UUID
    created_at: datetime
    display_name: str
    stripe_customer_id: str | None


class ProfileInsertRequest(BaseModel):
    # user id needs to be passed since its created from some "auth" table in the db 
    user_id: UUID
    tier_id: UUID
    display_name: str
    stripe_customer_id: str | None = None


class ProfileUpdateRequest(BaseModel):
    tier_id: UUID | None = None
    display_name: str | None = None
    stripe_customer_id: str | None = None
