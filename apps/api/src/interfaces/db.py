import json
import logging
import os
from enum import StrEnum, auto
from typing import Literal
from uuid import UUID

from dotenv import load_dotenv
from pydantic import ValidationError
from supabase import Client, create_client

from src.models import AgentModel, CrewModel, Message, Session, SessionStatus
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
) -> tuple[str, CrewModel] | tuple[Literal[False], Literal[False]]:
    """Get the compiled message and crew model for a given Crew ID."""
    logger.debug(f"Getting compiled message and crew model for {crew_id}")
    response = supabase.table("crews").select("*").eq("id", crew_id).execute()

    if len(response.data) == 0:
        logger.error(f"No compiled message and composition for {crew_id}")
        return False, False

    return parse_input(response.data[0])


def get_session(session_id: UUID) -> Session | None:
    """Get a session from the database."""
    logger.debug(f"Getting session {session_id}")
    response = supabase.table("sessions").select("*").eq("id", session_id).execute()
    if len(response.data) == 0:
        return None
    return Session(**response.data[0])


def post_session(session: Session) -> None:
    """Post a session to the database."""
    logger.debug(f"Posting session: {session}")
    supabase.table("sessions").insert(
        json.loads(json.dumps(session.model_dump(), default=str))
    ).execute()


def get_messages(session_id: UUID) -> list[Message] | None:
    """Get all messages for a given session."""
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
    """Post a message to the database."""
    logger.debug(f"Posting message: {message}")
    supabase.table("messages").insert(
        json.loads(json.dumps(message.model_dump(), default=str))
    ).execute()


def get_descriptions(agent_ids: list[UUID]) -> dict[UUID, list[str]] | None:
    """Get the description list for the given agent."""
    logger.debug(f"Getting description from agent_ids: {agent_ids}")
    response = (
        supabase.table("agents")
        .select("id", "description")
        .in_("id", agent_ids)
        .execute()
    )
    if len(response.data) < len(agent_ids):
        return None

    return {d["id"]: d["description"] for d in response.data}


def post_agents(agents: list[AgentModel]) -> None:
    """Post a list of agents to the database."""
    logger.debug(f"Posting agents: {agents}")
    supabase.table("agents").insert([agent.model_dump() for agent in agents]).execute()


def post_crew(message: Message, composition: CrewModel) -> None:
    post_agents(CrewModel.agents)
    # TODO: (Leon) Implement posting the rest of the crew


def get_tool_api_key(profile_id: UUID, api_key_type_id: UUID) -> str:
    """Gets an api key given a profile id and the type of api key."""
    response = (
        supabase.table("users_api_keys")
        .select("api_key")
        .filter("profile_id", "eq", str(profile_id))
        .filter("api_key_type_id", "eq", str(api_key_type_id))
        .execute()
    )
    return response.data[0]["api_key"]
    # This thing might be wrong, dont care right now


def update_status(session_id: UUID, status: SessionStatus) -> None:
    logger.debug(f"Updating session status: {status} for session: {session_id}")
    supabase.table("sessions").update({"status": status}).eq("id", session_id).execute()


if __name__ == "__main__":
    api_key = get_tool_api_key(
        UUID("93f3efda-672f-44a2-b64f-b7509e5f046f"),
        UUID("3b64fe26-20b9-4064-907e-f2708b5f1656"),
    )
    print(api_key)
