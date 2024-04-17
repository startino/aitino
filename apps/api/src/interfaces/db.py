import json
import logging
import os
from typing import Any, Literal, Optional
from uuid import UUID

from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import ValidationError
from supabase import Client, create_client

from src.models import (
    Agent,
    AgentInsertRequest,
    AgentUpdateModel,
    CrewInsertRequest,
    Crew,
    CrewUpdateRequest,
    Message,
    Profile,
    ProfileUpdateRequest,
    Session,
    SessionInsertRequest,
    Session,
    SessionStatus,
    SessionUpdateRequest,
    ProfileInsertRequest,
    APIKeyInsertRequest,
    APIKey,
    APIKeyType,
    APIKeyUpdateRequest,
    APIKeyType,
    MessageInsertRequest,
    Message,
    MessageUpdateRequest,
    Subscription,
    SubscriptionInsertRequest,
    SubscriptionUpdateRequest,
    SubscriptionGetRequest,
    Billing,
    BillingInsertRequest,
    BillingUpdateRequest,
    BillingGetRequest,
)

load_dotenv()
url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")


logger = logging.getLogger("root")


# keeping this function for now, since typing gets crazy with the sessions/run endpoint
# if it uses the "get_session_by_param" function
def get_session(session_id: UUID) -> Session | None:
    """Get a session from the database."""
    supabase: Client = create_client(url, key)
    logger.debug(f"Getting session {session_id}")
    response = supabase.table("sessions").select("*").eq("id", session_id).execute()
    if len(response.data) == 0:
        return None
    return Session(**response.data[0])


def get_sessions(
    profile_id: UUID | None = None,
    crew_id: UUID | None = None,
    title: str | None = None,
    status: str | None = None,
) -> list[Session]:
    """Gets session(s), filtered by what parameters are given"""
    supabase: Client = create_client(url, key)
    query = supabase.table("sessions").select("*")

    if profile_id:
        query = query.eq("profile_id", profile_id)

    if crew_id:
        query = query.eq("crew_id", crew_id)

    if title:
        query = query.eq("title", title)

    if status:
        query = query.eq("status", status)

    response = query.execute()

    return [Session(**data) for data in response.data]


def insert_session(content: SessionInsertRequest) -> Session:
    supabase: Client = create_client(url, key)
    logger.info(f"inserting session")
    response = (
        supabase.table("sessions")
        .insert(json.loads(content.model_dump_json()))
        .execute()
    )
    return Session(**response.data[0])


def update_session(session_id: UUID, content: SessionUpdateRequest) -> Session:
    supabase: Client = create_client(url, key)
    logger.info(f"updating session with id: {session_id}")
    response = (
        supabase.table("sessions")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("id", session_id)
        .execute()
    )
    return Session(**response.data[0])


def post_session(session: Session) -> None:
    """Post a session to the database."""
    supabase: Client = create_client(url, key)
    logger.debug(f"Posting session: {session}")
    supabase.table("sessions").insert(
        json.loads(json.dumps(session.model_dump(), default=str))
    ).execute()


def delete_session(session_id: UUID) -> Session:
    supabase: Client = create_client(url, key)
    response = supabase.table("sessions").delete().eq("id", session_id).execute()
    return Session(**response.data[0])


def get_messages(
    session_id: UUID | None = None,
    profile_id: UUID | None = None,
    recipient_id: UUID | None = None,
    sender_id: UUID | None = None,
) -> list[Message]:
    """Gets messages, filtered by what parameters are given"""
    supabase: Client = create_client(url, key)
    logger.debug(f"Getting messages")
    query = supabase.table("messages").select("*")

    if session_id:
        query = query.eq("session_id", session_id)

    if profile_id:
        query = query.eq("profile_id", profile_id)

    if recipient_id:
        query = query.eq("recipient_id", recipient_id)

    if sender_id:
        query = query.eq("sender_id", sender_id)

    response = query.execute()

    return [Message(**data) for data in response.data]


def get_message(message_id: UUID) -> Message:
    """Get a message by its id"""
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("messages").select("*").eq("id", message_id).single().execute()
    )
    return Message(**response.data)


# TODO: combine this function with the insert_message one, or use this post_message for both the endpoint and internal operations
def post_message(message: Message) -> None:
    """Post a message to the database."""
    supabase: Client = create_client(url, key)
    logger.debug(f"Posting message: {message}")
    supabase.table("messages").insert(
        json.loads(json.dumps(message.model_dump(), default=str))
    ).execute()


def insert_message(message: MessageInsertRequest) -> Message:
    """Posts a message like the post_message function, but uses a request model"""
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("messages")
        .insert(json.loads(message.model_dump_json(exclude_none=True)))
        .execute()
    )
    return Message(**response.data[0])


def delete_message(message_id: UUID) -> Message | None:
    """Deletes a message by an id (the primary key)"""
    supabase: Client = create_client(url, key)
    response = supabase.table("messages").delete().eq("id", message_id).execute()
    if len(response.data) == 0:
        return None

    return Message(**response.data[0])


def update_message(message_id: UUID, content: MessageUpdateRequest) -> Message | None:
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

    return Message(**response.data[0])


def get_subscriptions(
    profile_id: UUID | None = None,
    stripe_subscription_id: str | None = None,
) -> list[Subscription]:
    """Gets messages, filtered by what parameters are given"""
    supabase: Client = create_client(url, key)
    logger.debug(f"Getting subscriptions")
    query = supabase.table("subscriptions").select("*")

    if profile_id:
        query = query.eq("profile_id", profile_id)

    if stripe_subscription_id:
        query = query.eq("stripe_subscription_id", stripe_subscription_id)

    response = query.execute()

    return [Subscription(**data) for data in response.data]


def insert_subscription(subscription: SubscriptionInsertRequest) -> Subscription:
    """Posts a Subscription to the db"""
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("subscriptions")
        .insert(json.loads(subscription.model_dump_json(exclude_none=True)))
        .execute()
    )
    return Subscription(**response.data[0])


def delete_subscription(profile_id: UUID) -> Subscription | None:
    """Deletes a subscription by an id (the primary key)"""
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("subscriptions").delete().eq("profile_id", profile_id).execute()
    )
    if len(response.data) == 0:
        return None

    return Subscription(**response.data[0])


def update_subscription(
    profile_id: UUID, content: SubscriptionUpdateRequest
) -> Subscription | None:
    """Updates a subscription by an id"""
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("subscriptions")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("profile_id", profile_id)
        .execute()
    )
    if len(response.data) == 0:
        return None

    return Subscription(**response.data[0])


def get_billings(
    profile_id: UUID | None = None,
    stripe_payment_method: str | None = None,
) -> list[Billing]:
    """Gets messages, filtered by what parameters are given"""
    supabase: Client = create_client(url, key)
    logger.debug(f"Getting billings")
    query = supabase.table("billing_information").select("*")

    if profile_id:
        query = query.eq("profile_id", profile_id)

    if stripe_payment_method:
        query = query.eq("stripe_payment_method", stripe_payment_method)

    response = query.execute()

    return [Billing(**data) for data in response.data]


def insert_billing(billing: BillingInsertRequest) -> Billing:
    """Posts a Billing to the db"""
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("billing_information")
        .insert(json.loads(billing.model_dump_json(exclude_none=True)))
        .execute()
    )
    return Billing(**response.data[0])


def delete_billing(profile_id: UUID) -> Billing | None:
    """Deletes a billing by an id (the primary key)"""
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("billing_information")
        .delete()
        .eq("profile_id", profile_id)
        .execute()
    )
    if len(response.data) == 0:
        return None

    return Billing(**response.data[0])


def update_billing(profile_id: UUID, content: BillingUpdateRequest) -> Billing | None:
    """Updates a billing by an id"""
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("billing_information")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("profile_id", profile_id)
        .execute()
    )
    if len(response.data) == 0:
        return None

    return Billing(**response.data[0])


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


def post_agents(agents: list[Agent]) -> None:
    """Post a list of agents to the database."""
    supabase: Client = create_client(url, key)
    logger.debug(f"Posting agents: {agents}")
    supabase.table("agents").insert([agent.model_dump() for agent in agents]).execute()


def insert_crew(crew: CrewInsertRequest) -> Crew:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("crews").insert(json.loads(crew.model_dump_json())).execute()
    )
    return Crew(**response.data[0])
    # supabase.table("crews").upsert(crew.model_dump())


def update_crew(crew_id: UUID, content: CrewUpdateRequest) -> Crew:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("crews")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("id", crew_id)
        .execute()
    )
    return Crew(**response.data[0])


def get_crew(crew_id: UUID) -> Crew | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("crews").select("*").eq("id", crew_id).execute()
    if len(response.data) == 0:
        return None

    return Crew(**response.data[0])


def get_crews(
    profile_id: UUID | None = None,
    receiver_id: UUID | None = None,
    title: str | None = None,
    published: bool | None = None,
) -> list[Crew]:
    """Gets crews, filtered by what parameters are given"""
    supabase: Client = create_client(url, key)
    logger.debug(f"Getting crews")
    query = supabase.table("crews").select("*")

    if profile_id:
        query = query.eq("profile_id", profile_id)

    if receiver_id:
        query = query.eq("receiver_id", receiver_id)

    if title:
        query = query.eq("title", title)

    if published is not None:
        query = query.eq("published", published)

    response = query.execute()

    return [Crew(**data) for data in response.data]


def delete_crew(crew_id: UUID) -> Crew:
    supabase: Client = create_client(url, key)
    response = supabase.table("crews").delete().eq("id", crew_id).execute()
    return Crew(**response.data[0])


def get_api_key(api_key_id: UUID) -> APIKey:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("users_api_keys")
        .select("*, api_key_types(*)")
        .eq("id", api_key_id)
        .single()
        .execute()
    )

    api_key_type = APIKeyType(**response.data["api_key_types"])
    return APIKey(**response.data, api_key_type=api_key_type)


def get_tool_api_keys(
    profile_id: UUID, api_key_type_ids: list[str] | None = None
) -> dict[str, str]:
    """Gets all api keys for a profile id, if api_key_type_ids is given, only give api keys corresponding to those key types."""
    supabase: Client = create_client(url, key)
    # casted_ids = [str(api_key_type_id) for api_key_type_id in api_key_type_ids]
    query = (
        supabase.table("users_api_keys")
        .select("api_key", "api_key_type_id")
        .eq("profile_id", profile_id)
    )

    if api_key_type_ids:
        query = query.in_("api_key_type_id", api_key_type_ids)

    response = query.execute()
    return {data["api_key_type_id"]: data["api_key"] for data in response.data}


def get_api_key(api_key_id: UUID) -> APIKey | None:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("users_api_keys")
        .select("*, api_key_types(*)")
        .eq("id", api_key_id)
        .execute()
    )
    if len(response.data) == 0:
        return None

    api_key_type = APIKeyType(**response.data[0]["api_key_types"])
    return APIKey(**response.data[0], api_key_type=api_key_type)


def get_api_keys(
    profile_id: UUID | None = None,
    api_key_type_id: UUID | None = None,
    api_key: str | None = None,
) -> list[APIKey]:
    supabase: Client = create_client(url, key)
    query = supabase.table("users_api_keys").select("*, api_key_types(*)")

    if profile_id:
        query = query.eq("profile_id", profile_id)

    if api_key_type_id:
        query = query.eq("api_key_type_id", api_key_type_id)

    if api_key:
        query = query.eq("api_key", api_key)

    response = query.execute()

    api_keys = []
    for data in response.data:
        api_key_type = APIKeyType(**data["api_key_types"])
        api_keys.append(APIKey(**data, api_key_type=api_key_type))

    return api_keys


def insert_api_key(api_key: APIKeyInsertRequest) -> APIKey | None:
    supabase: Client = create_client(url, key)
    type_response = (
        supabase.table("api_key_types")
        .select("*")
        .eq("id", api_key.api_key_type_id)
        .execute()
    )
    if len(type_response.data) == 0:
        return None

    response = (
        supabase.table("users_api_keys")
        .insert(json.loads(api_key.model_dump_json()))
        .execute()
    )

    api_key_type = APIKeyType(**type_response.data[0])
    return APIKey(**response.data[0], api_key_type=api_key_type)


def delete_api_key(api_key_id: UUID) -> APIKey | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("users_api_keys").delete().eq("id", api_key_id).execute()
    if not len(response.data):
        return None

    type_response = (
        supabase.table("api_key_types")
        .select("*")
        .eq("id", response.data[0]["api_key_type_id"])
        .execute()
    )
    api_key_type = APIKeyType(**type_response.data[0])
    return APIKey(**response.data[0], api_key_type=api_key_type)


def update_api_key(api_key_id: UUID, api_key_update: APIKeyUpdateRequest) -> APIKey:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("users_api_keys")
        .update(json.loads(api_key_update.model_dump_json()))
        .eq("id", api_key_id)
        .execute()
    )
    type_response = (
        supabase.table("api_key_types")
        .select("*")
        .eq("id", response.data[0]["api_key_type_id"])
        .execute()
    )

    api_key_type = APIKeyType(**type_response.data[0])
    return APIKey(**response.data[0], api_key_type=api_key_type)


def get_api_key_types() -> list[APIKeyType]:
    supabase: Client = create_client(url, key)
    logger.debug("Getting all api key types")
    response = supabase.table("api_key_types").select("*").execute()
    return [APIKeyType(**data) for data in response.data]


def update_status(session_id: UUID, status: SessionStatus) -> None:
    supabase: Client = create_client(url, key)
    logger.debug(f"Updating session status: {status} for session: {session_id}")
    supabase.table("sessions").update({"status": status}).eq("id", session_id).execute()


def get_agents(
    profile_id: UUID | None = None,
    crew_id: UUID | None = None,
    published: bool | None = None,
) -> list[Agent] | None:
    """Gets agents, filtered by what parameters are given"""
    supabase: Client = create_client(url, key)
    query = supabase.table("agents").select("*")

    if profile_id:
        query = query.eq("profile_id", profile_id)

    # scuffed solution since agents dont have a crew id
    # prob gonna rework or remove this completely
    # also this crew_id param can't be used with any of the other parameters
    # since this doesn't build on the query var (it also returns so L)
    if crew_id:
        response = get_agents_from_crew(crew_id)
        if not response:
            return None

        return response

    if published is not None:
        query = query.eq("published", published)

    response = query.execute()

    return [Agent(**data) for data in response.data]


def get_agent(agent_id: UUID) -> Agent | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("agents").select("*").eq("id", agent_id).execute()
    if not response.data:
        return None

    return Agent(**response.data[0])


def get_agents_from_crew(crew_id: UUID) -> list[Agent] | None:
    supabase: Client = create_client(url, key)
    nodes = supabase.table("crews").select("nodes").eq("id", crew_id).execute()
    if len(nodes.data) == 0:
        return None

    response = (
        supabase.table("agents").select("*").in_("id", nodes.data[0]["nodes"]).execute()
    )
    return [Agent(**data) for data in response.data]


def insert_agent(content: AgentInsertRequest) -> Agent:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("agents").insert(json.loads(content.model_dump_json())).execute()
    )
    return Agent(**response.data[0])


def update_agents(agent_id: UUID, content: AgentUpdateModel) -> Agent:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("agents")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("id", agent_id)
        .execute()
    )
    return Agent(**response.data[0])


def delete_agent(agent_id: UUID) -> Agent:
    supabase: Client = create_client(url, key)
    response = supabase.table("agents").delete().eq("id", agent_id).execute()
    return Agent(**response.data[0])


def update_agent_tool(agent_id: UUID, tool_id: UUID) -> Agent:
    supabase: Client = create_client(url, key)
    agent_tools = supabase.table("agents").select("tools").eq("id", agent_id).execute()
    tool: dict = {"id": tool_id, "parameter": {}}

    agent_tools.data[0]["tools"].append(tool)
    formatted_tools = agent_tools.data[0]["tools"]
    response = (
        supabase.table("agents")
        .update(json.loads(json.dumps(formatted_tools, default=str)))
        .eq("id", agent_id)
        .execute()
    )
    return Agent(**response.data[0])


def get_profiles(
    tier_id: UUID | None = None,
    display_name: str | None = None,
    stripe_customer_id: str | None = None,
) -> list[Profile]:
    """Gets profiles, filtered by what parameters are given"""
    supabase: Client = create_client(url, key)
    query = supabase.table("profiles").select("*")

    if tier_id:
        query = query.eq("tier_id", tier_id)

    if display_name:
        query = query.eq("display_name", display_name)

    if stripe_customer_id:
        query = query.eq("stripe_customer_id", stripe_customer_id)

    response = query.execute()

    return [Profile(**data) for data in response.data]


def get_profile(profile_id: UUID) -> Profile | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("profiles").select("*").eq("id", profile_id).execute()
    if len(response.data) == 0:
        return None
    return Profile(**response.data[0])


def update_profile(profile_id: UUID, content: ProfileUpdateRequest) -> Profile:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("profiles")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("id", profile_id)
        .execute()
    )
    return Profile(**response.data[0])


def insert_profile(profile: ProfileInsertRequest) -> Profile:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("profiles")
        .insert(json.loads(profile.model_dump_json(exclude_none=True)))
        .execute()
    )
    return Profile(**response.data[0])


def delete_profile(profile_id: UUID) -> Profile:
    supabase: Client = create_client(url, key)
    response = supabase.table("profiles").delete().eq("id", profile_id).execute()
    return Profile(**response.data[0])


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
    # print(get_crew(UUID("bf9f1cdc-fb63-45e1-b1ff-9a1989373ce3")))
    ##print(insert_message(MessageRequestModel(
    #    session_id=UUID("ec4a9ae1-f4de-46cf-946d-956b3081c432"),
    #    profile_id=UUID("070c1d2e-9d72-4854-a55e-52ade5a42071"),
    #    content="hello test message",
    #    recipient_id=UUID("7c707c30-2cfe-46a0-afa7-8bcc38f9687e"),
    # )))

    # print(update_message(UUID("c3e4755b-141d-4f77-8ea8-924961ccf36d"), content=MessageUpdateRequest(content="wowzer")))
    # print(get_api_keys(api_key_type_id=UUID("3b64fe26-20b9-4064-907e-f2708b5f1656")))
    print(get_api_key_type_ids(["612ddae6-ecdd-4900-9314-1a2c9de6003d"]))
