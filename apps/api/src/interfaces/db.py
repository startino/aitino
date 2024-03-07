import json
import logging
import os
from uuid import UUID
from typing import Literal

from dotenv import load_dotenv
from pydantic import ValidationError
from supabase import Client, create_client

from src.models import Agent, Composition, Message, Session
from src.parser import parse_input_v0_2 as parse_input

load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

supabase: Client = create_client(url, key)

logger = logging.getLogger("root")


def get_compiled(
    crew_id: UUID,
) -> tuple[str, Composition] | tuple[Literal[False], Literal[False]]:
    """
    Get the compiled message and composition for a given Crew ID.
    """
    logger.debug(f"Getting compiled message and composition for {crew_id}")
    response = supabase.table("crews").select("*").eq("id", crew_id).execute()

    if len(response.data) == 0:
        logger.error(f"No compiled message and composition for {crew_id}")
        return False, False

    return parse_input(response.data[0])


def get_session(session_id: UUID) -> Session | None:
    """
    Get a session from the database.
    """
    logger.debug(f"Getting session {session_id}")
    response = supabase.table("sessions").select("*").eq("id", session_id).execute()
    if len(response.data) == 0:
        return None
    return Session(**response.data[0])


def post_session(session: Session) -> None:
    """
    Post a session to the database.
    """
    logger.debug(f"Posting session: {session}")
    supabase.table("sessions").insert(
        json.loads(json.dumps(session.model_dump(), default=str))
    ).execute()


def get_messages(session_id: UUID) -> list[Message] | None:
    """
    Get all messages for a given session.
    """
    logger.debug(f"Getting messages for session {session_id}")
    response = (
        supabase.table("messages").select("*").eq("session_id", session_id).execute()
    )

    messages = []

    try:
        messages = [Message(**msg) for msg in response.data]
    except ValidationError as e:
        logger.error(f"Error validating message: {e}")

    return messages


def post_message(message: Message) -> None:
    """
    Post a message to the database.
    """
    logger.debug(f"Posting message: {message}")
    supabase.table("messages").insert(
        json.loads(json.dumps(message.model_dump(), default=str))
    ).execute()


def post_agents(agents: list[Agent]) -> None:
    """
    Post a list of agents to the database.
    """
    logger.debug(f"Posting agents: {agents}")
    supabase.table("agents").insert([agent.model_dump() for agent in agents]).execute()


def post_crew(message: Message, composition: Composition) -> None:
    post_agents(Composition.agents)
    # TODO: (Leon) Implement posting the rest of the crew
