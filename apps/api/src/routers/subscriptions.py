import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import (
    RateLimitResponse,
    rate_limit,
    rate_limit_profile,
    rate_limit_tiered,
)
from src.interfaces import db
from src.models import (
    Subscription,
    MessageInsertRequest,
    Message,
    MessageUpdateRequest,
    SubscriptionGetRequest,
)

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

logger = logging.getLogger("root")


@router.get("/")
def get_subscriptions(q: SubscriptionGetRequest = Depends()) -> list[Subscription]:
    return db.get_messages(q.profile_id, q.stripe_payment_method)


@router.post("/")
def insert_message(message: MessageInsertRequest) -> Message:
    return db.insert_message(message)


@router.delete("/{message_id}")
def delete_message(message_id: UUID) -> Message:
    response = db.delete_message(message_id)
    if not response:
        raise HTTPException(404, "message not found")

    return response


@router.patch("/{message_id}")
def update_message(message_id: UUID, content: MessageUpdateRequest) -> Message:
    response = db.update_message(message_id, content)
    if not response:
        raise HTTPException(404, "message not found")

    return response


@router.get("/{message_id}")
def get_message(message_id: UUID) -> Message:
    return db.get_message(message_id)
