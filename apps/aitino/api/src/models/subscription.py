from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Subscription(BaseModel):
    profile_id: UUID
    stripe_subscription_id: str | None = None
    created_at: datetime


class SubscriptionInsertRequest(BaseModel):
    profile_id: UUID
    stripe_subscription_id: str | None = None


class SubscriptionUpdateRequest(BaseModel):
    stripe_subscription_id: str | None = None


class SubscriptionGetRequest(BaseModel):
    profile_id: UUID | None = None
    stripe_subscription_id: str | None = None
