import logging
from uuid import UUID

from fastapi import APIRouter
from src.interfaces import db
from src.models import CrewModel, Message, Session
from src.parser import parse_input_v0_2 as parse_input
from src.rest import comment_bot

router = APIRouter(prefix="/rest", tags=["rest"])

logger = logging.getLogger("root")


@router.get("/")
def publish_comment(submission_id, comment):
    comment_bot.publish_comment(submission_id, comment)
