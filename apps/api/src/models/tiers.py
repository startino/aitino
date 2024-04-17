from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Tier(BaseModel):
    id: UUID
    created_at: datetime
    period: int
    limit: int
    stripe_price_id: str | None = None
    name: str | None = None
    description: str | None = None
    slug: str | None = None
    image: str | None = None


class TierInsertRequest(BaseModel):
    period: int | None = None
    limit: int | None = None
    stripe_price_id: str | None = None
    name: str | None = None
    description: str | None = None
    slug: str | None = None
    image: str | None = None


class TierUpdateRequest(BaseModel):
    period: int | None = None
    limit: int | None = None
    stripe_price_id: str | None = None
    name: str | None = None
    description: str | None = None
    slug: str | None = None
    image: str | None = None


class TierGetRequest(BaseModel):
    id: UUID
    stripe_price_id: str | None = None
    name: str | None = None