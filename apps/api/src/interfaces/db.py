import json
import logging
import os
from uuid import UUID

from dotenv import load_dotenv
from supabase import Client, create_client

from src.models import (
    Agent,
    AgentInsertRequest,
    AgentUpdateRequest,
    APIKey,
    APIKeyInsertRequest,
    APIKeyUpdateRequest,
    APIProvider,
    Billing,
    BillingInsertRequest,
    BillingUpdateRequest,
    Crew,
    CrewInsertRequest,
    CrewUpdateRequest,
    Message,
    MessageInsertRequest,
    MessageUpdateRequest,
    Profile,
    ProfileInsertRequest,
    ProfileUpdateRequest,
    Session,
    SessionInsertRequest,
    SessionStatus,
    SessionUpdateRequest,
    Subscription,
    SubscriptionInsertRequest,
    SubscriptionUpdateRequest,
    Tier,
    TierInsertRequest,
    TierUpdateRequest,
    Tool,
    ToolInsertRequest,
    ToolUpdateRequest,
)

load_dotenv()
url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")


# keeping this function for now, since typing gets crazy with the sessions/run endpoint
# if it uses the "get_session_by_param" function
def get_session(session_id: UUID) -> Session | None:
    """Get a session from the database."""
    supabase: Client = create_client(url, key)
    logging.debug(f"Getting session {session_id}")
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
    logging.info("inserting session")
    response = (
        supabase.table("sessions")
        .insert(json.loads(content.model_dump_json()))
        .execute()
    )
    return Session(**response.data[0])


def update_session(session_id: UUID, content: SessionUpdateRequest) -> Session:
    supabase: Client = create_client(url, key)
    logging.info(f"updating session with id: {session_id}")
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
    logging.debug(f"Posting session: {session}")
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
    logging.debug("Getting messages")
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
    logging.debug(f"Posting message: {message}")
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
    """Gets subscriptions, filtered by what parameters are given"""
    supabase: Client = create_client(url, key)
    logging.debug("Getting subscriptions")
    query = supabase.table("subscriptions").select("*")

    if profile_id:
        query = query.eq("profile_id", profile_id)

    if stripe_subscription_id:
        query = query.eq("stripe_subscription_id", stripe_subscription_id)

    response = query.execute()

    return [Subscription(**data) for data in response.data]


def insert_subscription(subscription: SubscriptionInsertRequest) -> Subscription:
    """Posts a subscription to the db"""
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


def get_tier(id: UUID) -> Tier | None:
    """Gets tiers, filtered by what parameters are given"""
    supabase: Client = create_client(url, key)
    response = supabase.table("tiers").select("*").eq("id", id).execute()
    if len(response.data) == 0:
        return None

    return Tier(**response.data[0])


def insert_tier(tier: TierInsertRequest) -> Tier:
    """Posts a tier to the db"""
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("tiers")
        .insert(json.loads(tier.model_dump_json(exclude_none=True)))
        .execute()
    )
    return Tier(**response.data[0])


def delete_tier(id: UUID) -> Tier | None:
    """Deletes a tier by an id (the primary key)"""
    supabase: Client = create_client(url, key)
    response = supabase.table("tiers").delete().eq("id", id).execute()
    if len(response.data) == 0:
        return None

    return Tier(**response.data[0])


def update_tier(id: UUID, content: TierUpdateRequest) -> Tier | None:
    """Updates a tier by an id"""
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("tiers")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("id", id)
        .execute()
    )
    return Tier(**response.data[0])


def get_billing(
    profile_id: UUID,
) -> Billing | None:
    """Gets billings, filtered by what parameters are given"""
    supabase: Client = create_client(url, key)
    logging.debug("Getting billings")
    response = (
        supabase.table("billing_information")
        .select("*")
        .eq("profile_id", profile_id)
        .execute()
    )
    if len(response.data) == 0:
        return None

    return Billing(**response.data[0])


def insert_billing(billing: BillingInsertRequest) -> Billing:
    """Posts a billing to the db"""
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
    logging.debug(f"Getting description from agent_ids: {agent_ids}")
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
def get_api_provider_ids(tool_ids: list[str]) -> dict[str, str]:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("tools")
        .select("id", "api_provider_id")
        .in_("id", tool_ids)
        .execute()
    )
    return {data["id"]: data["api_provider_id"] for data in response.data}


def post_agents(agents: list[Agent]) -> None:
    """Post a list of agents to the database."""
    supabase: Client = create_client(url, key)
    logging.debug(f"Posting agents: {agents}")
    supabase.table("agents").insert([agent.model_dump() for agent in agents]).execute()


def insert_crew(crew: CrewInsertRequest) -> Crew:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("crews").insert(json.loads(crew.model_dump_json())).execute()
    )
    return Crew(**response.data[0])


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
    logging.debug("Getting crews")
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


def get_api_key(api_key_id: UUID) -> APIKey | None:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("users_api_keys")
        .select("*, api_providers(*)")
        .eq("id", api_key_id)
        .execute()
    )
    if len(response.data) == 0:
        return None

    api_provider = APIProvider(**response.data[0]["api_providers"])
    return APIKey(**response.data[0], api_provider=api_provider)


def get_api_keys(
    profile_id: UUID | None = None,
    api_provider_id: UUID | None = None,
    api_key: str | None = None,
) -> list[APIKey]:
    supabase: Client = create_client(url, key)
    query = supabase.table("users_api_keys").select("*, api_providers(*)")

    if profile_id:
        query = query.eq("profile_id", profile_id)

    if api_provider_id:
        query = query.eq("api_provider_id", api_provider_id)

    if api_key:
        query = query.eq("api_key", api_key)

    response = query.execute()

    api_keys = []
    for data in response.data:
        api_provider = APIProvider(**data["api_providers"])
        api_keys.append(APIKey(**data, api_provider=api_provider))

    return api_keys


def insert_api_key(api_key: APIKeyInsertRequest) -> APIKey | None:
    supabase: Client = create_client(url, key)
    provider_response = (
        supabase.table("api_providers")
        .select("*")
        .eq("id", api_key.api_provider_id)
        .execute()
    )
    if len(provider_response.data) == 0:
        return None

    response = (
        supabase.table("users_api_keys")
        .insert(json.loads(api_key.model_dump_json()))
        .execute()
    )

    api_provider = APIProvider(**provider_response.data[0])
    return APIKey(**response.data[0], api_provider=api_provider)


def delete_api_key(api_key_id: UUID) -> APIKey | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("users_api_keys").delete().eq("id", api_key_id).execute()
    if not len(response.data):
        return None

    provider_response = (
        supabase.table("api_providers")
        .select("*")
        .eq("id", response.data[0]["api_provider_id"])
        .execute()
    )
    api_provider = APIProvider(**provider_response.data[0])
    return APIKey(**response.data[0], api_provider=api_provider)


def update_api_key(api_key_id: UUID, api_key_update: APIKeyUpdateRequest) -> APIKey:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("users_api_keys")
        .update(json.loads(api_key_update.model_dump_json()))
        .eq("id", api_key_id)
        .execute()
    )
    provider_response = (
        supabase.table("api_providers")
        .select("*")
        .eq("id", response.data[0]["api_provider_id"])
        .execute()
    )

    api_provider = APIProvider(**provider_response.data[0])
    return APIKey(**response.data[0], api_provider=api_provider)


def get_api_providers() -> list[APIProvider]:
    supabase: Client = create_client(url, key)
    logging.debug("Getting all api providers")
    response = supabase.table("api_providers").select("*").execute()
    return [APIProvider(**data) for data in response.data]


def update_status(session_id: UUID, status: SessionStatus) -> None:
    supabase: Client = create_client(url, key)
    logging.debug(f"Updating session status: {status} for session: {session_id}")
    supabase.table("sessions").update({"status": status}).eq("id", session_id).execute()


def get_agent(agent_id: UUID) -> Agent | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("agents").select("*").eq("id", agent_id).execute()
    if not response.data:
        return None

    return Agent(**response.data[0])


def get_agents(
    profile_id: UUID | None = None,
    published: bool | None = None,
) -> list[Agent]:
    """Gets agents, filtered by what parameters are given"""
    supabase: Client = create_client(url, key)
    query = supabase.table("agents").select("*")

    if profile_id:
        query = query.eq("profile_id", profile_id)

    if published is not None:
        query = query.eq("published", published)

    response = query.execute()

    return [Agent(**data) for data in response.data]


def get_agents_from_crew(crew_id: UUID) -> list[Agent] | None:
    supabase: Client = create_client(url, key)
    agents = supabase.table("crews").select("agents").eq("id", crew_id).execute()
    if len(agents.data) == 0:
        return None

    response = (
        supabase.table("agents")
        .select("*")
        .in_("id", agents.data[0]["agents"])
        .execute()
    )
    return [Agent(**data) for data in response.data]


def insert_agent(content: AgentInsertRequest) -> Agent:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("agents").insert(json.loads(content.model_dump_json())).execute()
    )
    return Agent(**response.data[0])


def update_agents(agent_id: UUID, content: AgentUpdateRequest) -> Agent:
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


def get_tool(tool_id: UUID) -> Tool | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("tools").select("*").eq("id", tool_id).execute()
    if len(response.data) == 0:
        return None

    return Tool(**response.data[0])


def get_tools(
    name: str | None = None,
    api_provider_id: UUID | None = None,
) -> list[Tool]:
    supabase: Client = create_client(url, key)
    query = supabase.table("tools").select("*")

    if name:
        query = query.eq("name", name)

    if api_provider_id:
        query = query.eq("api_provider_id", api_provider_id)

    response = query.execute()

    return [Tool(**data) for data in response.data]


def update_tool(tool_id: UUID, content: ToolUpdateRequest) -> Tool:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("tools")
        .update(json.loads(content.model_dump_json(exclude_none=True)))
        .eq("id", tool_id)
        .execute()
    )
    return Tool(**response.data[0])


def insert_tool(tool: ToolInsertRequest) -> Tool:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("tools")
        .insert(json.loads(tool.model_dump_json(exclude_none=True)))
        .execute()
    )
    return Tool(**response.data[0])


def delete_tool(tool_id: UUID) -> Tool | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("tools").delete().eq("id", tool_id).execute()
    if len(response.data) == 0:
        return None

    return Tool(**response.data[0])


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


def get_tool_api_keys(
    profile_id: UUID, api_provider_ids: list[str] | None = None
) -> dict[str, str]:
    """Gets all api keys for a profile id, if api_provider_ids is given, only give api keys corresponding to those providers."""
    supabase: Client = create_client(url, key)
    query = (
        supabase.table("users_api_keys")
        .select("api_key", "api_provider_id")
        .eq("profile_id", profile_id)
    )

    if api_provider_ids:
        query = query.in_("api_provider_id", api_provider_ids)

    response = query.execute()
    return {data["api_provider_id"]: data["api_key"] for data in response.data}


def get_profile(profile_id: UUID) -> Profile | None:
    supabase: Client = create_client(url, key)
    response = supabase.table("profiles").select("*").eq("id", profile_id).execute()
    if len(response.data) == 0:
        return None
    return Profile(**response.data[0])


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
    profile_dict = json.loads(profile.model_dump_json(exclude_none=True))
    profile_dict["funding"] = 100
    response = supabase.table("profiles").insert(profile_dict).execute()
    return Profile(**response.data[0])


def delete_profile(profile_id: UUID) -> Profile:
    supabase: Client = create_client(url, key)
    response = supabase.table("profiles").delete().eq("id", profile_id).execute()
    return Profile(**response.data[0])


def update_funding(profile_id: UUID, new_funding: int) -> int:
    supabase: Client = create_client(url, key)
    response = (
        supabase.table("profiles")
        .update({"funding": new_funding})
        .eq("id", profile_id)
        .execute()
    )
    return response.data[0]["funding"]


if __name__ == "__main__":
    from src.models import Session

    # print(add_crew_to_agent(UUID("7c707c30-2cfe-46a0-afa7-8bcc38f9687e"), UUID("4cf4de3c-30cd-4ac1-bfd6-a26aeb0fec8c")))
