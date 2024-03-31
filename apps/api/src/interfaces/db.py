import json
import logging
import os
from enum import StrEnum, auto
from typing import Any, Literal
from uuid import UUID

from dotenv import load_dotenv
from pydantic import ValidationError
from supabase import Client, create_client

from src.models import (
    AgentModel,
    AgentRequestModel,
    AgentResponseModel,
    AgentUpdateModel,
    CrewModel,
    CrewRequestModel,
    CrewResponseModel,
    CrewUpdateModel,
    Message,
    Session,
    SessionRequest,
    SessionResponse,
    SessionStatus,
    SessionUpdate,
)
from src.models.profile import Profile
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


def get_sessions(
    profile_id: UUID | None = None, session_id: UUID | None = None
) -> list[Session]:
    """Gets all sessions for given profile id."""
    logger.debug(f"Getting all sessions from profile_id: {profile_id}")
    query = supabase.table("sessions").select("*")
    if profile_id:
        query = query.eq("profile_id", profile_id)

    if session_id:
        query = query.eq("id", session_id)

    response = query.execute()

    sessions = []
    if len(response.data) == 0:
        return sessions

    try:
        sessions = [Session(**session) for session in response.data]
    except ValidationError as e:
        logger.error(f"Error validating session: {e}")

    return sessions


def insert_session(content: SessionRequest) -> SessionResponse:
    logger.info(f"inserting session")
    response = (
        supabase.table("sessions")
        .insert(json.loads(content.model_dump_json()))
        .execute()
    )
    return SessionResponse(**response.data[0])


def update_session(session_id: UUID, content: SessionUpdate) -> SessionResponse:
    logger.info(f"updating session with id: {session_id}")
    response = (
        supabase.table("sessions")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("id", session_id)
        .execute()
    )
    return SessionResponse(**response.data[0])


# TODO: refactor this thing, maybe session protocol so session can be both the internal session object and the response/request object
def post_session(session: Session) -> None:
    """Post a session to the database."""
    logger.debug(f"Posting session: {session}")
    supabase.table("sessions").insert(
        json.loads(json.dumps(session.model_dump(), default=str))
    ).execute()


def delete_session(session_id: UUID) -> None:
    supabase.table("sessions").delete().eq("id", session_id).execute()


def get_messages(session_id: UUID) -> list[Message]:
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


def insert_crew(crew: CrewRequestModel) -> CrewResponseModel:
    response = (
        supabase.table("crews").insert(json.loads(crew.model_dump_json())).execute()
    )
    return CrewResponseModel(**response.data[0])
    # supabase.table("crews").upsert(crew.model_dump())


def update_crew(crew_id: UUID, content: CrewUpdateModel) -> CrewResponseModel:
    response = (
        supabase.table("crews")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("id", crew_id)
        .execute()
    )
    return CrewResponseModel(**response.data[0])


def get_crew_from_id(crew_id: UUID) -> CrewResponseModel:
    response = supabase.table("crews").select("*").eq("id", crew_id).execute()
    return CrewResponseModel(**response.data[0])


def get_published_crews() -> list[CrewResponseModel]:
    response = supabase.table("crews").select("*").eq("published", "TRUE").execute()
    return [CrewResponseModel(**data) for data in response.data]


def get_user_crews(profile_id: UUID, ascending: bool = True) -> list[CrewResponseModel]:
    response = (
        supabase.table("crews")
        .select("*")
        .eq("profile_id", profile_id)
        .order("created_at", desc=(not ascending))
        .execute()
    )
    return [CrewResponseModel(**data) for data in response.data]


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


def update_status(session_id: UUID, status: SessionStatus) -> None:
    logger.debug(f"Updating session status: {status} for session: {session_id}")
    supabase.table("sessions").update({"status": status}).eq("id", session_id).execute()


def get_profile_from_id(profile_id: UUID) -> Profile | None:
    response = supabase.table("profiles").select("*").eq("id", profile_id).execute()
    if len(response.data) == 0:
        return None
    return Profile(**response.data[0])


def get_published_agents() -> list[AgentResponseModel]:
    response = supabase.table("agents").select("*").eq("published", "TRUE").execute()
    return [AgentResponseModel(**data) for data in response.data]


def get_users_agents(profile_id: UUID) -> list[AgentResponseModel]:
    response = (
        supabase.table("agents").select("*").eq("profile_id", profile_id).execute()
    )
    return [AgentResponseModel(**data) for data in response.data]


def get_agent_by_id(agent_id: UUID) -> AgentResponseModel | None:
    response = supabase.table("agents").select("*").eq("id", agent_id).execute()
    if not response.data:
        return None

    return AgentResponseModel(**response.data[0])


def get_agents_from_crew(crew_id: UUID) -> list[AgentResponseModel]:
    nodes = supabase.table("crews").select("nodes").eq("id", crew_id).execute()
    response = (
        supabase.table("agents").select("*").in_("id", nodes.data[0]["nodes"]).execute()
    )
    return [AgentResponseModel(**data) for data in response.data]


def insert_agent(content: AgentRequestModel) -> AgentResponseModel:
    response = (
        supabase.table("agents").insert(json.loads(content.model_dump_json())).execute()
    )
    return AgentResponseModel(**response.data[0])


def update_agents(content: AgentUpdateModel) -> AgentResponseModel:
    response = (
        supabase.table("agents")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .execute()
    )
    return AgentResponseModel(**response.data[0])


def delete_agent(agent_id: UUID) -> AgentResponseModel:
    response = supabase.table("agents").delete().eq("id", agent_id).execute()
    return AgentResponseModel(**response.data[0])


if __name__ == "__main__":
    from src.models import Session

    print(
        insert_session(
            SessionRequest(
                crew_id=UUID("1c11a9bf-748f-482b-9746-6196f136401a"),
                profile_id=UUID("070c1d2e-9d72-4854-a55e-52ade5a42071"),
                title="hello",
            )
        )
    )
