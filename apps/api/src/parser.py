import json
import logging
from typing import Literal
from uuid import UUID

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


def parse_input_v0_2(
    input_data: dict,
) -> tuple[str, CrewModel] | tuple[Literal[False], Literal[False]]:
    logger.debug("Parsing input v0.2")

    def _parse_composition(nodes: dict) -> CrewModel | Literal[False]:
        logger.debug("Parsing composition")
        composition = CrewModel(
            reciever_id="auto",
            agents=list(),
        )
        for node in nodes:
            if node["type"] == "agent":
                agent_id = node["id"]

                # TODO: Optimize by creating a get_agents method which takes a
                # list of agent_ids and get's them all with a single database
                # call
                agent = get_agent(agent_id)

                if not agent:
                    logger.error(f"Agent {agent_id} not found")
                    return False

                composition.agents.append(agent)
        return composition

    def _parse_prompts(nodes: dict) -> str:
        logger.debug("Parsing prompts")
        prompt = []
        for node in nodes:
            if node["type"] == "prompt":
                prompt.append(node["data"]["content"])
        return "\n\n".join(prompt)

    nodes = input_data["nodes"]
    composition = _parse_composition(nodes)
    if not composition:
        logger.error("Failed to parse composition")
        return False, False
    message = _parse_prompts(nodes)
    return message, composition


def parse_input_v0_1(input_data: dict) -> tuple[str, CrewModel]:
    def _parse_composition(nodes: dict) -> CrewModel:
        composition = CrewModel(
            reciever_id="auto",
            agents=list(),
        )

        for node in nodes:
            if node["type"] == "agent":
                agent = Agent(
                    id=node["id"],
                    name=node["data"]["name"],
                    role=node["data"]["role"],
                    system_message=node["data"]["prompt"],
                    model=node["data"]["model"]["value"],
                )
                composition.agents.append(agent)
        return composition

    def _parse_prompts(nodes: dict) -> str:
        prompt = []
        for node in nodes:
            if node["type"] == "prompt":
                prompt.append(node["data"]["content"])
        return "\n\n".join(prompt)

    nodes = input_data["nodes"]
    composition = _parse_composition(nodes)
    message = _parse_prompts(nodes)
    return message, composition


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
    return message, CrewModel(reciever_id="auto", agents=agents)


if __name__ == "__main__":
    message, composition = parse_autobuild(
        '"composition": {"message": "create a website for designing your own lamps","agents":[{"role": "UI/UX Designer","system_message": "Design the user interface and user experience for the lamp designing website. This includes creating wireframes, mockups, and interactive prototypes to ensure a user-friendly and visually appealing design."},{"role": "React Developer","system_message": "Develop the front-end of the lamp designing website using React. This includes implementing the UI/UX designs into functional web pages, ensuring responsiveness, and integrating any necessary APIs for lamp design functionalities."},{"role": "Backend Developer","system_message": "Create and manage the server, database, and application logic for the lamp designing website. This includes setting up the server, creating database schemas, and developing APIs for user management, lamp design storage, and retrieval."},{"role": "Quality Assurance Engineer","system_message": "Test the lamp designing website for bugs, performance issues, and usability. This includes conducting both automated and manual tests to ensure the website is reliable, efficient, and user-friendly."}]}'
    )
