from datetime import UTC, datetime
import logging
from typing import cast
from uuid import UUID, uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from src import mock as mocks
from src.crew import AutogenCrew
from src.dependencies import (
    RateLimitResponse,
    rate_limit,
    rate_limit_profile,
    rate_limit_tiered,
)
from src.interfaces import db
from src.models import (
    CrewProcessed,
    Crew,
    Message,
    SessionRunRequest,
    SessionRunResponse,
    Session,
    Session,
    SessionUpdateRequest,
    SessionGetRequest,
    SessionStatus,
)
from src.models.session import SessionInsertRequest
from src.parser import process_crew, get_processed_crew_by_id

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
)

logger = logging.getLogger("root")


@router.get("/")
def get_sessions(
    q: SessionGetRequest = Depends()
) -> list[Session]:
    return db.get_sessions(q.profile_id, q.crew_id, q.title, q.status)


@router.get("/{session_id}")
def get_session(session_id: UUID) -> Session:
    response = db.get_session(session_id)
    if response is None:
        raise HTTPException(500, "failed validation")
        # not sure if 500 is correct, but this is failed validation on the returned data, so 
        # it makes sense in my mind to raise a server error for that
    
    return response
    # pretty sure this response object will always be a session, so casting it to stop typing errors
    
    
@router.patch("/{session_id}")
def update_session(session_id: UUID, content: SessionUpdateRequest) -> Session:
    return db.update_session(session_id, content)


@router.post("/", status_code=201)
def insert_session(content: SessionInsertRequest) -> Session:
    return db.insert_session(content)


# apparently status code 204 doesnt allow response bodies, so i'll have to look into that
@router.delete("/{session_id}")
def delete_session(session_id: UUID) -> Session:
    if not db.get_session(session_id):
        raise HTTPException(404, "session not found")

    return db.delete_session(session_id)


@router.post("/run")
# change to tiered rate limiter later, its annoying for testing so its currently using profile rate limiter
async def run_crew(
    request: SessionRunRequest,
    background_tasks: BackgroundTasks,
    mock: bool = False,
) -> Session:
    if request.reply and not request.session_id:
        raise HTTPException(
            status_code=400,
            detail="If a reply is provided, a session_id must also be provided.",
        )
    if request.session_id and not request.reply:
        raise HTTPException(
            status_code=400,
            detail="If a session_id is provided, a reply must also be provided.",
        )

    if mock:
        message, crew_model = process_crew(Crew(**mocks.crew_model))
    else:
        message, crew_model = get_processed_crew_by_id(request.crew_id)

    if request.reply:
        message = request.reply

    if not message or not crew_model:
        raise HTTPException(status_code=400, detail=f"Failed to get crew with id {id}")

    session = db.get_session(request.session_id) if request.session_id else None
    cached_messages = (
        db.get_messages(request.session_id) if request.session_id else None
    )

    if request.session_id and not session:
        raise HTTPException(
            status_code=400,
            detail=f"Session with id {request.session_id} not found",
        )

    if request.session_id and not cached_messages:
        raise HTTPException(
            status_code=400,
            detail=f"Session with id {request.session_id} found, but has no messages",
        )

    if session is None:
        session = Session(
            id=uuid4(),
            created_at=datetime.now(tz=UTC),
            crew_id=request.crew_id,
            profile_id=request.profile_id,
            title=request.session_title,
            reply="",
            last_opened_at=datetime.now(tz=UTC),
            status=SessionStatus.RUNNING
        )
        db.post_session(session)

    async def on_reply(
        recipient_id: UUID,
        sender_id: UUID,
        content: str,
        role: str,
    ) -> None:
        message = Message(
            session_id=session.id,
            profile_id=session.profile_id,
            recipient_id=recipient_id,
            sender_id=sender_id,
            content=content,
            role=role,
        )
        logger.debug(f"on_reply: {message}")
        db.post_message(message)

    try:
        crew = AutogenCrew(session.profile_id, session, crew_model, on_reply)
    except ValueError as e:
        logger.error(e)
        raise HTTPException(400, "crew model bad input")

    background_tasks.add_task(crew.run, message, messages=cached_messages)

    return session
