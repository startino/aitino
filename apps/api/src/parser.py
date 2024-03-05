import logging
import json

from re import A
from typing import Literal

from src.crew import Agent, Composition
from src.interfaces import db

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


def parse_autobuild(input_data: str) -> tuple[str, Composition] | tuple[Literal[False], Literal[False]]:
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

