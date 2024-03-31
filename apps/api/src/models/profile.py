from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Profile(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    tier_id: UUID
    created_at: str
    display_name: str
    stripe_customer_id: str | None
