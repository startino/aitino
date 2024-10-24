import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.interfaces import db
from src.models import (
    Subscription,
    SubscriptionGetRequest,
    SubscriptionInsertRequest,
    SubscriptionUpdateRequest,
)

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

logger = logging.getLogger("root")


@router.get("/")
def get_subscriptions(q: SubscriptionGetRequest = Depends()) -> list[Subscription]:
    return db.get_subscriptions(q.profile_id, q.stripe_subscription_id)


@router.post("/", status_code=201)
def insert_subscription(subscription: SubscriptionInsertRequest) -> Subscription:
    return db.insert_subscription(subscription)


@router.delete("/{id}")
def delete_subscription(id: UUID) -> Subscription:
    response = db.delete_subscription(id)
    if not response:
        raise HTTPException(404, "stripe subscription id not found")

    return response


@router.patch("/{id}")
def update_subscription(id: UUID, content: SubscriptionUpdateRequest) -> Subscription:
    response = db.update_subscription(id, content)
    if not response:
        raise HTTPException(404, "message not found")

    return response
