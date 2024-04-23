import logging
from datetime import UTC, datetime
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
    Crew,
    CrewProcessed,
    Message,
    Session,
    SessionGetRequest,
    SessionRunRequest,
    SessionRunResponse,
    SessionStatus,
    SessionUpdateRequest,
)
from src.models.session import SessionInsertRequest
from src.parser import get_processed_crew_by_id, process_crew

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
)


@router.get("/")
def get_sessions(q: SessionGetRequest = Depends()) -> list[Session]:
    return db.get_sessions(q.profile_id, q.crew_id, q.title, q.status)


@router.get("/{id}")
def get_session(id: UUID) -> Session:
    response = db.get_session(id)
    if response is None:
        raise HTTPException(500, "failed validation")
        # not sure if 500 is correct, but this is failed validation on the returned data, so
        # it makes sense in my mind to raise a server error for that

    return response
    # pretty sure this response object will always be a session, so casting it to stop typing errors


@router.patch("/{id}")
def update_session(id: UUID, content: SessionUpdateRequest) -> Session:
    return db.update_session(id, content)


@router.post("/", status_code=201)
def insert_session(content: SessionInsertRequest) -> Session:
    return db.insert_session(content)


# apparently status code 204 doesnt allow response bodies, so i'll have to look into that
@router.delete("/{id}")
def delete_session(id: UUID) -> Session:
    if not db.get_session(id):
        raise HTTPException(404, "session not found")

    return db.delete_session(id)


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
        request.crew_id = UUID("1c11a9bf-748f-482b-9746-6196f136401a")
        request.profile_id = UUID("070c1d2e-9d72-4854-a55e-52ade5a42071")
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
            status=SessionStatus.RUNNING,
        )
        db.post_session(session)

    async def on_reply(
        recipient_id: UUID,
        sender_id: UUID,
        content: str,
        role: str,
    ) -> None:
        message = Message(
            id=uuid4(),
            session_id=session.id,
            profile_id=session.profile_id,
            recipient_id=recipient_id,
            sender_id=sender_id,
            content=content,
            role=role,
            created_at=datetime.now(tz=UTC),
        )
        logging.debug(f"on_reply: {message}")
        db.post_message(message)

    try:
        crew = AutogenCrew(session.profile_id, session, crew_model, on_reply)
    except Exception as e:
        db.delete_session(session.id)
        logging.error(f"got error when running crew: {e}")
        raise e

    background_tasks.add_task(crew.run, message, messages=cached_messages)

    return session
