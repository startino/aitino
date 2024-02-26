import logging
import os
import json
from uuid import UUID

from dotenv import load_dotenv
from pydantic import ValidationError
from supabase import Client, create_client

from ..maeve import Composition
from ..models import Message, Session
from ..parser import parse_input

load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

supabase: Client = create_client(url, key)

logger = logging.getLogger("root")


def get_complied(maeve_id: UUID) -> tuple[str, Composition] | tuple[None, None]:
    """
    Get the complied message and composition for a given Maeve ID.
    """
    response = supabase.table("maeve_nodes").select("*").eq("id", maeve_id).execute()

    if len(response.data) == 0:
        return None, None

    return parse_input(response.data[0])


def get_session(session_id: UUID) -> Session | None:
    """
    Get a session from the database.
    """
    response = supabase.table("sessions").select("*").eq("id", session_id).execute()
    if len(response.data) == 0:
        return None
    return Session(**response.data[0])


def post_session(session: Session) -> None:
    """
    Post a session to the database.
    """
    supabase.table("sessions").upsert(
        json.loads(json.dumps(session.model_dump(), default=str))
    ).execute()


def get_messages(session_id: UUID) -> list[Message] | None:
    """
    Get all messages for a given session.
    """
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
    supabase.table("messages").upsert(
        json.loads(json.dumps(message.model_dump(), default=str))
    ).execute()
