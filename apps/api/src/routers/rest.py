import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException
from src.models import CrewResponseModel, Message, Session
from src.parser import parse_input_v0_2 as parse_input
from src.rest import comment_bot
from src.rest.interfaces import db
from src.rest.models import PublishCommentRequest, PublishCommentResponse

router = APIRouter(prefix="/rest", tags=["rest"])

logger = logging.getLogger("root")


@router.post("/")
def publish_comment(publish_request: PublishCommentRequest):
    updated_content = comment_bot.publish_comment(
        publish_request.lead_id, 
        publish_request.comment, 
        publish_request.reddit_username, 
        publish_request.reddit_password,
    )
    if updated_content is None:
        raise HTTPException(404, "lead not found")

    return updated_content

@router.get("/")
def get_leads() -> list[PublishCommentResponse]:
    return db.get_all_leads()
