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
    SubscriptionInsertRequest,
    SubscriptionUpdateRequest,
    SubscriptionGetRequest,
)

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

logger = logging.getLogger("root")


@router.get("/")
def get_subscriptions(q: SubscriptionGetRequest = Depends()) -> list[Subscription]:
    return db.get_subscriptions(q.profile_id, q.stripe_subscription_id)


@router.post("/", status_code=201)
def insert_subscription(subscription: SubscriptionInsertRequest) -> Subscription:
    return db.insert_subscription(subscription)


@router.delete("/{profile_id}")
def delete_subscription(profile_id: UUID) -> Subscription:
    response = db.delete_subscription(profile_id)
    if not response:
        raise HTTPException(404, "stripe subscription id not found")

    return response


@router.patch("/{profile_id}")
def update_subscription(
    profile_id: UUID, content: SubscriptionUpdateRequest
) -> Subscription:
    response = db.update_subscription(profile_id, content)
    if not response:
        raise HTTPException(404, "message not found")

    return response


#
#
# @router.get("/{message_id}")
# def get_message(message_id: UUID) -> Message:
#     return db.get_message(message_id)
