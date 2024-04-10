import logging
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, FastAPI, HTTPException

from src import mock as mocks
from src.crew import Crew
from src.dependencies import (
    RateLimitResponse,
    rate_limit,
    rate_limit_profile,
    rate_limit_tiered,
)
from src.interfaces import db
from src.models import CrewModel, Message, Session, MessageRequestModel, MessageResponseModel, MessageUpdateModel
from src.parser import parse_input_v0_2 as parse_input

router = APIRouter(prefix="/messages", tags=["messages"])

logger = logging.getLogger("root")


@router.get("/")
def get_messages(session_id: UUID) -> list[Message]:
    return db.get_messages(session_id)


@router.post("/")
def insert_message(message: MessageRequestModel) -> MessageResponseModel:
    return db.insert_message(message)


@router.delete("/{message_id}")
def delete_message(message_id: UUID) -> MessageResponseModel:
    return db.delete_message(message_id)


@router.patch("/{message_id}")
def update_message(message_id: UUID, content: MessageUpdateModel) -> MessageResponseModel:
    return db.update_message(message_id, content)