import json
import logging
from typing import Literal

from src.models import Agent, Composition

logger = logging.getLogger("root")
logging.basicConfig(level=logging.DEBUG)


def parse_composition(nodes: dict) -> Composition:
    composition = Composition(
        reciever_id="auto",
        agents=list(),
    )

    for node in nodes:
        if node["type"] == "agent":
            agent = Agent(
                id=node["id"],
                name=node["data"]["name"],
                job_title=node["data"]["job_title"],
                system_message=node["data"]["prompt"],
                model=node["data"]["model"]["value"],
            )
            composition.agents.append(agent)
    return composition


def parse_prompts(nodes: dict) -> str:
    prompt = []
    for node in nodes:
        if node["type"] == "prompt":
            prompt.append(node["data"]["content"])
    return "\n\n".join(prompt)


def parse_input(input_data: dict) -> tuple[str, Composition]:
    nodes = input_data["nodes"]
    composition = parse_composition(nodes)
    message = parse_prompts(nodes)
    return message, composition


def parse_autobuild(
    input_data: str,
) -> tuple[str, Composition] | tuple[Literal[False], Literal[False]]:
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
    return message, Composition(reciever_id="auto", agents=agents)


if __name__ == "__main__":
    message, composition = parse_autobuild(
        '"composition": {"message": "create a website for designing your own lamps","agents":[{"job_title": "UI/UX Designer","system_message": "Design the user interface and user experience for the lamp designing website. This includes creating wireframes, mockups, and interactive prototypes to ensure a user-friendly and visually appealing design."},{"job_title": "React Developer","system_message": "Develop the front-end of the lamp designing website using React. This includes implementing the UI/UX designs into functional web pages, ensuring responsiveness, and integrating any necessary APIs for lamp design functionalities."},{"job_title": "Backend Developer","system_message": "Create and manage the server, database, and application logic for the lamp designing website. This includes setting up the server, creating database schemas, and developing APIs for user management, lamp design storage, and retrieval."},{"job_title": "Quality Assurance Engineer","system_message": "Test the lamp designing website for bugs, performance issues, and usability. This includes conducting both automated and manual tests to ensure the website is reliable, efficient, and user-friendly."}]}'
    )
