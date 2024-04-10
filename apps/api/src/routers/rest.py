import logging
from uuid import UUID

from fastapi import APIRouter
from src.interfaces import db
from src.models import CrewModel, Message, Session, PublishCommentRequest
from src.parser import parse_input_v0_2 as parse_input
from src.rest import comment_bot, reddit_bot

router = APIRouter(prefix="/rest", tags=["rest"])

logger = logging.getLogger("root")


@router.post("/")
def start_reddit_stream():
    reddit_bot.start_reddit_stream()


@router.post("/publish_comment")
def publish_comment(publish_request: PublishCommentRequest):
    comment_bot.publish_comment(
        publish_request.lead_id,
        publish_request.comment,
        publish_request.reddit_username,
        publish_request.reddit_password,
    )
