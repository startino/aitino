import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from postgrest.exceptions import APIError

from src.dependencies import (
    RateLimitResponse,
    rate_limit,
    rate_limit_profile,
    rate_limit_tiered,
)
from src.interfaces import db
from src.models import (
    Message,
    MessageGetRequest,
    MessageInsertRequest,
    MessageUpdateRequest,
)

router = APIRouter(prefix="/messages", tags=["messages"])

logger = logging.getLogger("root")


@router.get("/")
def get_messages(q: MessageGetRequest = Depends()) -> list[Message]:
    return db.get_messages(q.session_id, q.profile_id, q.recipient_id, q.sender_id)


@router.post("/", status_code=201)
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
    response = db.get_message(message_id)
    if not response:
        raise HTTPException(404, "message not found")

    return response
