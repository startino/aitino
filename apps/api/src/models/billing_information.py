from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Billing(BaseModel):
    profile_id: UUID
    stripe_payment_method: str | None = None
    description: str | None = None
    created_at: datetime


class BillingInsertRequest(BaseModel):
    profile_id: UUID
    stripe_payment_method: str | None = None
    description: str | None = None


class BillingUpdateRequest(BaseModel):
    stripe_payment_method: str | None = None
    description: str | None = None
