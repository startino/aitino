from pydantic import BaseModel


class Agent(BaseModel):
    id: str
    name: str
    job_title: str
    system_message: str
    model: str


class Composition(BaseModel):
    reciever_id: str
    agents: list[Agent]


def parse_composition(nodes) -> Composition:
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


def parse_prompts(nodes) -> str:
    prompt = []
    for node in nodes:
        if node["type"] == "prompt":
            prompt.append(node["data"]["content"])
    return "\n\n".join(prompt)


def parse_input(input_data) -> tuple[str, Composition]:
    nodes = input_data["nodes"]
    composition = parse_composition(nodes)
    message = parse_prompts(nodes)
    return message, composition
