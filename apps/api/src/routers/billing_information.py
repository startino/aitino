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
    Billing,
    BillingInsertRequest,
    BillingUpdateRequest,
)

router = APIRouter(prefix="/billing", tags=["billings"])

logger = logging.getLogger("root")


@router.get("/{id}")
def get_billings(id: UUID) -> Billing:
    response = db.get_billing(id)
    if not response:
        raise HTTPException(404, "billing information not found")

    return response


@router.post("/")
def insert_billing(subscription: BillingInsertRequest) -> Billing:
    return db.insert_billing(subscription)


@router.delete("/{profile_id}")
def delete_billing(profile_id: UUID) -> Billing:
    response = db.delete_billing(profile_id)
    if not response:
        raise HTTPException(404, "stripe subscription id not found")

    return response


@router.patch("/{profile_id}")
def update_billing(profile_id: UUID, content: BillingUpdateRequest) -> Billing:
    response = db.update_billing(profile_id, content)
    if not response:
        raise HTTPException(404, "message not found")

    return response


#
#
# @router.get("/{message_id}")
# def get_message(message_id: UUID) -> Message:
#     return db.get_message(message_id)