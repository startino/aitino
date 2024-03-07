from pydantic import BaseModel

from .agent import Agent


class Composition(BaseModel):
    reciever_id: str
    agents: list[Agent]
