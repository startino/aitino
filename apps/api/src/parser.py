import json
import logging
from typing import Literal
from uuid import UUID, uuid4

from src.models import Agent, CrewModel

logger = logging.getLogger("root")
logging.basicConfig(level=logging.DEBUG)


# Below is the code from src/interfaces/db.py
import os  # noqa: E402

from dotenv import load_dotenv  # noqa: E402
from supabase import Client  # noqa: E402
from supabase import create_client

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
    logger.debug(f"Getting agent {agent_id}")
    response = supabase.table("agents").select("*").eq("id", agent_id).execute()
    if len(response.data) == 0:
        logger.error(f"No agent found for {agent_id}")
        return None
    return Agent(**response.data[0])


def get_agents(agent_ids: list[UUID]) -> list[Agent]:
    logger.debug(f"getting agents from agent_ids: {agent_ids}")
    response = supabase.table("agents").select("*").in_("id", agent_ids).execute()
    return [Agent(**agent) for agent in response.data]


def parse_input_v0_2(
    input_data: dict,
) -> tuple[str, CrewModel]:
    logger.debug("Parsing input v0.2")

    agent_ids: list[UUID] = input_data["nodes"]
    reciever_id: UUID = input_data["reciever_id"]

    crew_model = CrewModel(
        reciever_id=reciever_id,
        agents=get_agents(agent_ids),
    )
    message: str = input_data["prompt"]["content"]
    return message, crew_model


def parse_autobuild(
    input_data: str,
) -> tuple[str, CrewModel] | tuple[Literal[False], Literal[False]]:
    input_data = input_data.replace("\n", "")
    try:
        dict_input = json.loads(input_data)
        print(dict_input)

    except json.JSONDecodeError as e:
        logger.debug("failed input decoding, trying fix")
        dict_input = json.loads("{%s}" % input_data)
        print(dict_input)
    # agents: list[Agent] = list()
    if "composition" not in dict_input.keys():
        return False, False
    if "agents" not in dict_input["composition"].keys():
        return False, False

    message = dict_input["composition"]["message"]
    agents = [Agent(**agent) for agent in dict_input["composition"]["agents"]]
    return message, CrewModel(reciever_id=uuid4(), agents=agents)


if __name__ == "__main__":
    message, composition = parse_autobuild(
        '"composition": {"message": "create a website for designing your own lamps","agents":[{"role": "UI/UX Designer","system_message": "Design the user interface and user experience for the lamp designing website. This includes creating wireframes, mockups, and interactive prototypes to ensure a user-friendly and visually appealing design."},{"role": "React Developer","system_message": "Develop the front-end of the lamp designing website using React. This includes implementing the UI/UX designs into functional web pages, ensuring responsiveness, and integrating any necessary APIs for lamp design functionalities."},{"role": "Backend Developer","system_message": "Create and manage the server, database, and application logic for the lamp designing website. This includes setting up the server, creating database schemas, and developing APIs for user management, lamp design storage, and retrieval."},{"role": "Quality Assurance Engineer","system_message": "Test the lamp designing website for bugs, performance issues, and usability. This includes conducting both automated and manual tests to ensure the website is reliable, efficient, and user-friendly."}]}'
    )
