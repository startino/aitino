import json
import logging
import os
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
    ProfileResponseModel,
    ProfileUpdateModel,
    Session,
    SessionRequest,
    SessionResponse,
    SessionStatus,
    SessionUpdate,
    ProfileRequestModel,
    APIKeyRequestModel,
    APIKeyResponseModel,
    APIKeyTypeModel,
    APIKeyUpdateModel,
    APIKeyTypeResponseModel,
    MessageRequestModel,
    MessageResponseModel,
    MessageUpdateModel,
)
from src.parser import parse_input_v0_2 as parse_input

load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")


logger = logging.getLogger("root")


def get_compiled(
    crew_id: UUID,
) -> tuple[str, CrewModel] | tuple[Literal[False], Literal[False]]:
    """Get the compiled message and crew model for a given Crew ID."""
    supabase: Client = create_client(url, key)
    logger.debug(f"Getting compiled message and crew model for {crew_id}")
    response = supabase.table("crews").select("*").eq("id", crew_id).execute()

    if len(response.data) == 0:
        logger.error(f"No compiled message and composition for {crew_id}")
        return False, False

    return parse_input(response.data[0])


def get_session(session_id: UUID) -> Session | None:
    """Get a session from the database."""
    supabase: Client = create_client(url, key)
    logger.debug(f"Getting session {session_id}")
    response = supabase.table("sessions").select("*").eq("id", session_id).execute()
    if len(response.data) == 0:
        return None
    return Session(**response.data[0])


def get_sessions_by_profile(profile_id: UUID) -> list[Session]:
    """Gets all sessions for given profile id."""
    supabase: Client = create_client(url, key)
    logger.debug(f"Getting all sessions from profile_id: {profile_id}")
    response = supabase.table("sessions").select("*").eq("profile_id", profile_id).execute()

    sessions = []
    if len(response.data) == 0:
        return sessions

    try:
        sessions = [Session(**session) for session in response.data]
    except ValidationError as e:
        logger.error(f"Error validating session: {e}")

    return sessions


def get_session_by_id(session_id: UUID) -> Session | None:
    """Gets all sessions for given session id."""
    supabase: Client = create_client(url, key)
    response = supabase.table("sessions").select("*").eq("id", session_id).single().execute()
    try:
        return Session(**response.data)
    except ValidationError as e:
        logger.error(f"Error validating session: {e}")


def insert_session(content: SessionRequest) -> SessionResponse:
    supabase: Client = create_client(url, key)
    logger.info(f"inserting session")
    response = (
        supabase.table("sessions")
        .insert(json.loads(content.model_dump_json()))
        .execute()
    )
    return SessionResponse(**response.data[0])


def update_session(session_id: UUID, content: SessionUpdate) -> SessionResponse:
    supabase: Client = create_client(url, key)
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
    supabase: Client = create_client(url, key)
    logger.debug(f"Posting session: {session}")
    supabase.table("sessions").insert(
        json.loads(json.dumps(session.model_dump(), default=str))
    ).execute()


def delete_session(session_id: UUID) -> None:
    supabase: Client = create_client(url, key)
    supabase.table("sessions").delete().eq("id", session_id).execute()


def get_messages(session_id: UUID) -> list[Message]:
    """Get all messages for a given session."""
    supabase: Client = create_client(url, key)
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


def get_message_by_id(message_id: UUID) -> MessageResponseModel:
    """Get a message by its id"""
    supabase: Client = create_client(url, key)
    response = supabase.table("messages").select("*").eq("id", message_id).single().execute()
    return MessageResponseModel(**response.data)
    
# TODO: combine this function with the insert_message one, or use this post_message for both the endpoint and internal operations
def post_message(message: Message) -> None:
    """Post a message to the database."""
    supabase: Client = create_client(url, key)
    logger.debug(f"Posting message: {message}")
    supabase.table("messages").insert(
        json.loads(json.dumps(message.model_dump(), default=str))
    ).execute()


def insert_message(message: MessageRequestModel) -> MessageResponseModel:
    """Posts a message like the post_message function, but uses a request model"""
    supabase: Client = create_client(url, key)
    response = supabase.table("messages").insert(json.loads(message.model_dump_json(exclude_none=True))).execute()
    return MessageResponseModel(**response.data[0])


def delete_message(message_id: UUID) -> MessageResponseModel | None:
    """Deletes a message by an id (the primary key)"""
    supabase: Client = create_client(url, key)
    response = supabase.table("messages").delete().eq("id", message_id).execute()
    if len(response.data) == 0:
        return None

    return MessageResponseModel(**response.data[0])


def update_message(message_id: UUID, content: MessageUpdateModel) -> MessageResponseModel | None:
    """Updates a message by an id"""
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("messages")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("id", message_id)
        .execute()
    )
    if len(response.data) == 0:
        return None

    return MessageResponseModel(**response.data[0])


def get_descriptions(agent_ids: list[UUID]) -> dict[UUID, list[str]] | None:
    """Get the description list for the given agent."""
    supabase: Client = create_client(url, key)
    logger.debug(f"Getting description from agent_ids: {agent_ids}")
    response = (
        supabase.table("agents")
        .select("id", "description")
        .in_("id", agent_ids)
        .execute()
    )
    if len(response.data) < len(agent_ids):
        return None

    return {data["id"]: data["description"] for data in response.data}


# typed as list[str] even though its technically UUID,
# since its typed this way in the get_tool_ids_from_agents
def get_api_key_type_ids(tool_ids: list[str]) -> dict[str, str]:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("tools")
        .select("id", "api_key_type_id")
        .in_("id", tool_ids)
        .execute()
    )
    return {data["id"]: data["api_key_type_id"] for data in response.data}


def post_agents(agents: list[AgentModel]) -> None:
    """Post a list of agents to the database."""
    supabase: Client = create_client(url, key)
    logger.debug(f"Posting agents: {agents}")
    supabase.table("agents").insert([agent.model_dump() for agent in agents]).execute()


def insert_crew(crew: CrewRequestModel) -> CrewResponseModel:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("crews").insert(json.loads(crew.model_dump_json())).execute()
    )
    return CrewResponseModel(**response.data[0])
    # supabase.table("crews").upsert(crew.model_dump())


def update_crew(crew_id: UUID, content: CrewUpdateModel) -> CrewResponseModel:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("crews")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("id", crew_id)
        .execute()
    )
    return CrewResponseModel(**response.data[0])


def get_crew_from_id(crew_id: UUID) -> CrewResponseModel:
    supabase: Client = create_client(url, key)
    response = supabase.table("crews").select("*").eq("id", str(crew_id)).single().execute()
    
    return CrewResponseModel(**response.data)


def get_published_crews() -> list[CrewResponseModel]:
    supabase: Client = create_client(url, key)
    response = supabase.table("crews").select("*").eq("published", "TRUE").execute()
    return [CrewResponseModel(**data) for data in response.data]


def get_user_crews(profile_id: UUID, ascending: bool = False) -> list[CrewResponseModel]:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("crews")
        .select("*")
        .eq("profile_id", profile_id)
        .order("created_at", desc=(not ascending))
        .execute()
    )
    return [CrewResponseModel(**data) for data in response.data]


def get_tool_api_keys(
    profile_id: UUID, api_key_type_ids: list[str] | None = None
) -> dict[str, str]:
    """Gets all api keys for a profile id, if api_key_type_ids is given, only give api keys corresponding to those key types."""
    # casted_ids = [str(api_key_type_id) for api_key_type_id in api_key_type_ids]
    supabase: Client = create_client(url, key)
    query = (
        supabase.table("users_api_keys")
        .select("api_key", "api_key_type_id")
        .eq("profile_id", profile_id)
    )

    if api_key_type_ids:
        query = query.in_("api_key_type_id", api_key_type_ids)

    response = query.execute()
    return {data["api_key_type_id"]: data["api_key"] for data in response.data}


def get_api_keys(profile_id: UUID) -> list[APIKeyResponseModel]:
    supabase: Client = create_client(url, key)
    response = supabase.table("users_api_keys").select("*, api_key_types(*)").eq("profile_id", profile_id).execute()
    api_keys = []
    for data in response.data:
        api_key_type = APIKeyTypeModel(**data["api_key_types"])
        api_keys.append(APIKeyResponseModel(**data, api_key_type=api_key_type))
        
    return api_keys #{data["api_key_type_id"]: data["api_key"] for data in response.data}


def insert_api_key(api_key: APIKeyRequestModel) -> APIKeyResponseModel:
    supabase: Client = create_client(url, key)
    response = supabase.table("users_api_keys").insert(json.loads(api_key.model_dump_json())).execute()
    return APIKeyResponseModel(**response.data[0])


def delete_api_key(api_key_id: UUID) -> APIKeyResponseModel | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("users_api_keys").delete().eq("id", api_key_id).execute()
    if not len(response.data):
        return None
    return APIKeyResponseModel(**response.data[0])


def update_api_key(api_key_id: UUID, api_key_update: APIKeyUpdateModel) -> APIKeyResponseModel:
    supabase: Client = create_client(url, key)
    response = supabase.table("users_api_keys").update(json.loads(api_key_update.model_dump_json())).eq("id", api_key_id).execute()
    return APIKeyResponseModel(**response.data[0])


def get_api_key_types() -> list[APIKeyTypeResponseModel]:
    supabase: Client = create_client(url, key)
    logger.debug("Getting all api key types")
    response = supabase.table("api_key_types").select("*").execute()
    return  [APIKeyTypeResponseModel(**data) for data in response.data]


def update_status(session_id: UUID, status: SessionStatus) -> None:
    supabase: Client = create_client(url, key)
    logger.debug(f"Updating session status: {status} for session: {session_id}")
    supabase.table("sessions").update({"status": status}).eq("id", session_id).execute()


def get_published_agents() -> list[AgentResponseModel]:
    supabase: Client = create_client(url, key)
    response = supabase.table("agents").select("*").eq("published", "TRUE").execute()
    return [AgentResponseModel(**data) for data in response.data]


def get_users_agents(profile_id: UUID) -> list[AgentResponseModel]:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("agents").select("*").eq("profile_id", profile_id).execute()
    )
    return [AgentResponseModel(**data) for data in response.data]


def get_agent_by_id(agent_id: UUID) -> AgentResponseModel | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("agents").select("*").eq("id", agent_id).execute()
    if not response.data:
        return None

    return AgentResponseModel(**response.data[0])


def get_agents_from_crew(crew_id: UUID) -> list[AgentResponseModel]:
    supabase: Client = create_client(url, key)
    nodes = supabase.table("crews").select("nodes").eq("id", crew_id).execute()
    response = (
        supabase.table("agents").select("*").in_("id", nodes.data[0]["nodes"]).execute()
    )
    return [AgentResponseModel(**data) for data in response.data]


def insert_agent(content: AgentRequestModel) -> AgentResponseModel:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("agents").insert(json.loads(content.model_dump_json())).execute()
    )
    return AgentResponseModel(**response.data[0])


def update_agents(content: AgentUpdateModel) -> AgentResponseModel:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("agents")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .execute()
    )
    return AgentResponseModel(**response.data[0])


def delete_agent(agent_id: UUID) -> AgentResponseModel:
    supabase: Client = create_client(url, key)
    response = supabase.table("agents").delete().eq("id", agent_id).execute()
    return AgentResponseModel(**response.data[0])


def get_profiles() -> list[ProfileResponseModel]:
    supabase: Client = create_client(url, key)
    response = supabase.table("profiles").select("*").execute()
    return [ProfileResponseModel(**data) for data in response.data]


def get_profile_from_id(profile_id: UUID) -> ProfileResponseModel | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("profiles").select("*").eq("id", profile_id).execute()
    if len(response.data) == 0:
        return None
    return ProfileResponseModel(**response.data[0])


def update_profile(
    profile_id: UUID, content: ProfileUpdateModel
) -> ProfileResponseModel:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("profiles")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("id", profile_id)
        .execute()
    )
    return ProfileResponseModel(**response.data[0])


def insert_profile(profile: ProfileRequestModel) -> ProfileResponseModel:
    supabase: Client = create_client(url, key)
    response = supabase.table("profiles").insert(json.loads(profile.model_dump_json(exclude_none=True))).execute()
    return ProfileResponseModel(**response.data[0])


# def get_keys_from_profile(profile_id: UUID) -> dict[str, str]:
#   supabase.table("users_api_keys").select("api_key", "api_key_type_id").eq("profile_id", profile_id)
if __name__ == "__main__":
    from src.models import Session

#    print(
#        insert_session(
#            SessionRequest(
#                crew_id=UUID("1c11a9bf-748f-482b-9746-6196f136401a"),
#                profile_id=UUID("070c1d2e-9d72-4854-a55e-52ade5a42071"),
#                title="hello",
#            )
#        )
#    )
#
    print(get_crew_from_id(UUID("bf9f1cdc-fb63-45e1-b1ff-9a1989373ce3")))
    ##print(insert_message(MessageRequestModel(
    #    session_id=UUID("ec4a9ae1-f4de-46cf-946d-956b3081c432"),
    #    profile_id=UUID("070c1d2e-9d72-4854-a55e-52ade5a42071"),
    #    content="hello test message",
    #    recipient_id=UUID("7c707c30-2cfe-46a0-afa7-8bcc38f9687e"),
    #)))

    print(delete_message(UUID('0e30e657-2ee1-482f-ab07-1952dc4d20fb')))
    print(update_message(UUID("c3e4755b-141d-4f77-8ea8-924961ccf36d"), content=MessageUpdateModel(content="wowzer")))