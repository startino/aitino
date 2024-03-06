import logging
import os
import json
from uuid import UUID

from dotenv import load_dotenv
from pydantic import ValidationError
from supabase import Client, create_client

from src.crew import Agent, Composition
from src.models import Message, Session
from src.parser import parse_input, parse_autobuild


load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

supabase: Client = create_client(url, key)

logger = logging.getLogger("root")


def get_complied(crew_id: UUID) -> tuple[str, Composition] | tuple[None, None]:
    """
    Get the complied message and composition for a given Crew ID.
    """
    logger.debug(f"Getting complied message and composition for {crew_id}")
    response = supabase.table("crews").select("*").eq("id", crew_id).execute()

    if len(response.data) == 0:
        return None, None

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
    supabase.table("agents").insert(
        [agent.model_dump() for agent in agents]
    ).execute()


def post_crew(message: Message, composition: Composition) -> None:
    post_agents(Composition.agents)
    # TODO: (Leon) Implement posting the rest of the crew

#message, composition = parse_autobuild('"composition": {"message": "create a website for designing your own lamps","agents":[{"job_title": "UI/UX Designer","system_message": "Design the user interface and user experience for the lamp designing website. This includes creating wireframes, mockups, and interactive prototypes to ensure a user-friendly and visually appealing design."},{"job_title": "React Developer","system_message": "Develop the front-end of the lamp designing website using React. This includes implementing the UI/UX designs into functional web pages, ensuring responsiveness, and integrating any necessary APIs for lamp design functionalities."},{"job_title": "Backend Developer","system_message": "Create and manage the server, database, and application logic for the lamp designing website. This includes setting up the server, creating database schemas, and developing APIs for user management, lamp design storage, and retrieval."},{"job_title": "Quality Assurance Engineer","system_message": "Test the lamp designing website for bugs, performance issues, and usability. This includes conducting both automated and manual tests to ensure the website is reliable, efficient, and user-friendly."}]}') 
#if composition:
#    agent_list = composition.agents
#post_agents(agent_list)