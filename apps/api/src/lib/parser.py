import json
import logging
# Below is the code from src/interfaces/db.py
import os  # noqa: E402
from typing import Literal, cast
from uuid import UUID, uuid4

from dotenv import load_dotenv  # noqa: E402
from fastapi import HTTPException
from supabase import Client  # noqa: E402
from supabase import create_client

from src.interfaces import db
from src.models import Agent, Crew, CrewProcessed, ValidCrew

load_dotenv()
url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")
if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

supabase: Client = create_client(url, key)


# TODO: Move this to the db.py file, will make a circular import for now but I'll fix later
# - Jonas
def get_agent(agent_id: UUID) -> Agent | None:
    """
    Get an agent from the database.
    """
    logging.debug(f"Getting agent {agent_id}")
    response = supabase.table("agents").select("*").eq("id", agent_id).execute()
    if len(response.data) == 0:
        logging.error(f"No agent found for {agent_id}")
        return None
    return Agent(**response.data[0])


def get_agents_by_ids(agent_ids: list[UUID]) -> list[Agent]:
    logging.debug(f"getting agents from agent_ids: {agent_ids}")
    response = supabase.table("agents").select("*").in_("id", agent_ids).execute()
    return [Agent(**agent) for agent in response.data]


def process_crew(crew: Crew) -> tuple[str, CrewProcessed]:
    logging.debug("Processing crew")
    agent_ids: list[UUID] = crew.agents

    _crew, error = validate_crew(crew)

    if error or not _crew:
        raise HTTPException(400, error)

    crew_model = CrewProcessed(
        receiver_id=_crew.receiver_id,
        agents=get_agents_by_ids(agent_ids),
    )

    message = _crew.prompt
    return message, crew_model


def validate_crew(crew: Crew) -> tuple[ValidCrew | None, str]:
    logging.debug("Validating crew")

    agent_ids: list[UUID] = crew.agents
    agents = get_agents_by_ids(agent_ids)

    if not crew.receiver_id:
        return None, "Crew has no receiver id"
    if not crew.prompt or crew.prompt == "":
        return None, "Crew has no prompt"
    if len(agents) == 0:
        return None, "Crew has no agents"

    # Validate agents
    for agent in agents:
        if agent.title == "":
            return None, "Agent has no title"
        if agent.role == "":
            return None, f'Agent "{agent.title}" has no role'
        if agent.system_message == "":
            return None, f'Agent "{agent.title}" has no system message'

    return ValidCrew(**crew.model_dump()), ""


def get_processed_crew_by_id(crew_id: UUID) -> tuple[str, CrewProcessed]:
    logging.debug("Getting processed crew by id")
    crew = db.get_crew(crew_id)
    if not crew:
        raise HTTPException(404, "Crew not found")
        # TODO: remove this raise here, should be further up (so in the endpoints where this function is called) -Leon
    return process_crew(crew)


def parse_autobuild(
    input_data: str,
) -> tuple[str, CrewProcessed] | tuple[Literal[False], Literal[False]]:
    input_data = input_data.replace("\n", "")
    try:
        dict_input = json.loads(input_data)
        print(dict_input)

    except json.JSONDecodeError as e:
        logging.debug("failed input decoding, trying fix")
        dict_input = json.loads("{%s}" % input_data)
        print(dict_input)
    # agents: list[Agent] = list()
    if "composition" not in dict_input.keys():
        return False, False
    if "agents" not in dict_input["composition"].keys():
        return False, False

    message = dict_input["composition"]["message"]
    agents = [Agent(**agent) for agent in dict_input["composition"]["agents"]]
    return message, CrewProcessed(receiver_id=uuid4(), agents=agents)


if __name__ == "__main__":
    # message, composition = parse_autobuild(
    #    '"composition": {"message": "create a website for designing your own lamps","agents":[{"role": "UI/UX Designer","system_message": "Design the user interface and user experience for the lamp designing website. This includes creating wireframes, mockups, and interactive prototypes to ensure a user-friendly and visually appealing design."},{"role": "React Developer","system_message": "Develop the front-end of the lamp designing website using React. This includes implementing the UI/UX designs into functional web pages, ensuring responsiveness, and integrating any necessary APIs for lamp design functionalities."},{"role": "Backend Developer","system_message": "Create and manage the server, database, and application logic for the lamp designing website. This includes setting up the server, creating database schemas, and developing APIs for user management, lamp design storage, and retrieval."},{"role": "Quality Assurance Engineer","system_message": "Test the lamp designing website for bugs, performance issues, and usability. This includes conducting both automated and manual tests to ensure the website is reliable, efficient, and user-friendly."}]}'
    # )
    print(get_agents_by_ids([UUID("7c707c30-2cfe-46a0-afa7-8bcc38f9687e")]))
