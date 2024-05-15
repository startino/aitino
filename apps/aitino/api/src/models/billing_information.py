from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


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
