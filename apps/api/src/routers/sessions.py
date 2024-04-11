import logging
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, HTTPException

from src import mock as mocks
from src.crew import Crew
from src.dependencies import (
    RateLimitResponse,
    rate_limit,
    rate_limit_profile,
    rate_limit_tiered,
)
from src.interfaces import db
from src.models import (
    CrewModel,
    Message,
    RunRequestModel,
    RunResponse,
    Session,
    Session,
    SessionUpdate,
)
from src.models.session import SessionRequest
from src.parser import parse_input_v0_2 as parse_input

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
)

logger = logging.getLogger("root")


@router.get("/", response_model=list[Session])
def get_sessions_by_profile(by_profile: UUID) -> list[Session]:
    return db.get_sessions_by_profile(profile_id=by_profile)


@router.get("/{session_id}")
def get_session_by_id(session_id: UUID) -> Session:
    response = db.get_session_by_id(session_id=session_id)

    if response is None:
        raise HTTPException(500, "failed validation")
        # not sure if 500 is correct, but this is failed validation on the returned data, so 
        # it makes sense in my mind to call that a server error
    
    return response


@router.patch("/{session_id}", response_model=Session)
def update_session(session_id: UUID, content: SessionUpdate) -> Session:
    return db.update_session(session_id, content)


@router.post("/", response_model=Session)
def insert_session(content: SessionRequest) -> Session:
    return db.insert_session(content)


@router.delete("/{session_id}", status_code=204)
def delete_session(session_id: UUID) -> None:
    if not get_session_by_id(session_id):
        raise HTTPException(404, "session not found")

    db.delete_session(session_id)


@router.post("/run", response_model=RunResponse)
# change to tiered rate limiter later, its annoying for testing so its currently using profile rate limiter
async def run_crew(
    run_request: RunRequestModel,
    background_tasks: BackgroundTasks,
    mock: bool = False,
) -> RunResponse:
    if run_request.reply and not run_request.session_id:
        raise HTTPException(
            status_code=400,
            detail="If a reply is provided, a session_id must also be provided.",
        )
    if run_request.session_id and not run_request.reply:
        raise HTTPException(
            status_code=400,
            detail="If a session_id is provided, a reply must also be provided.",
        )

    if mock:
        message, crew_model = parse_input(mocks.crew_model)
    else:
        message, crew_model = db.get_compiled(run_request.id)

    if run_request.reply:
        message = run_request.reply

    if not message or not crew_model:
        raise HTTPException(status_code=400, detail=f"Failed to get crew with id {id}")

    session = db.get_session(run_request.session_id) if run_request.session_id else None
    cached_messages = (
        db.get_messages(run_request.session_id) if run_request.session_id else None
    )

    if run_request.session_id and not session:
        raise HTTPException(
            status_code=400,
            detail=f"Session with id {run_request.session_id} not found",
        )

    if run_request.session_id and not cached_messages:
        raise HTTPException(
            status_code=400,
            detail=f"Session with id {run_request.session_id} found, but has no messages",
        )

    if session is None:
        session = Session(
            crew_id=run_request.id,
            profile_id=run_request.profile_id,
            title=run_request.session_title,
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
        crew = Crew(session.profile_id, session, crew_model, on_reply)
    except ValueError as e:
        logger.error(e)
        raise HTTPException(400, "crew model bad input")

    background_tasks.add_task(crew.run, message, messages=cached_messages)

    return RunResponse(status="success", session=session)
