import logging
import asyncio
from asyncio import Queue
from typing import Any, cast

import autogen
from autogen.cache import Cache
from pydantic import BaseModel

from .models import CodeExecutionConfig, Message

logger = logging.getLogger("root")


class Agent(BaseModel):
    id: str
    name: str
    job_title: str
    system_message: str
    model: str


class Composition(BaseModel):
    reciever_id: str
    agents: list[Agent]


class Crew:
    def __init__(
        self,
        composition: Composition,
        on_message: Any | None = None,
        base_model: str = "gpt-4-turbo-preview",
        seed: int = 41,
    ):
        self.seed = seed
        self.on_reply = on_message
        if not self.validate_composition(composition):
            raise ValueError("composition is invalid")

        self.user_proxy = autogen.UserProxyAgent(
            name="Admin",
            system_message="""Reply TERMINATE if the task has been solved at full satisfaction. If you instead require more information reply TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
            max_consecutive_auto_reply=1,
            human_input_mode="NEVER",
            default_auto_reply="Reply TERMINATE if the task has been solved at full satisfaction. If you instead require more information reply TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.",
            code_execution_config=CodeExecutionConfig(
                work_dir=f".cache/{self.seed}/scripts"
            ).model_dump(),
        )

        self.agents: list[autogen.ConversableAgent | autogen.Agent] = (
            self.create_agents(composition)
        )

        self.base_config_list = autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": [base_model],
            },
        )
        self.base_config = {
            "seed": seed,
            "temperature": 0,
            "config_list": self.base_config_list,
            "timeout": 120,
        }

    async def _on_reply(
        self,
        recipient: autogen.ConversableAgent,
        messages: list[dict] | None = None,
        sender: Agent | None = None,
        config: Any | None = None,
    ) -> tuple[bool, Any | None]:
        if self.on_reply:
            await self.on_reply(recipient, messages, sender, config)

        return False, None

    def validate_composition(self, composition: Composition) -> bool:
        if len(composition.agents) == 0:
            return False

        # Validate agents
        for agent in composition.agents:
            if agent.id == "":
                return False
            if agent.model == "":
                return False
            if agent.job_title == "":
                return False
            if agent.name == "":
                return False
            if agent.system_message == "":
                return False
        return True

    def create_agents(
        self, composition: Composition
    ) -> list[autogen.ConversableAgent | autogen.Agent]:
        agents = []

        for agent in composition.agents:
            config_list = autogen.config_list_from_json(
                "OAI_CONFIG_LIST",
                filter_dict={
                    "model": [agent.model],
                },
            )

            config = {
                "seed": self.seed,
                "temperature": 0,
                "config_list": config_list,
                "timeout": 120,
            }
            agent = autogen.AssistantAgent(
                name=f"""{agent.job_title.replace(' ', '')}-{agent.name.replace(' ', '')}""",
                system_message=f"""{agent.job_title} {agent.name}. {agent.system_message}. Reply TERMINATE if the task has been solved at full satisfaction. If you instead require more information reply TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
                llm_config=config,
            )

            if self.on_reply:
                agent.register_reply([autogen.Agent, None], self._on_reply)

            agents.append(agent)
        return agents

    async def run(
        self,
        message: str,
        messages: list[Message] | None = None,
        q: Queue | None = None,
        job_done: object | None = None,
    ) -> None:

        # convert Message list to dict list
        dict_messages = [m.model_dump() for m in (messages if messages else [])]

        groupchat = autogen.GroupChat(
            agents=self.agents + [self.user_proxy],
            messages=dict_messages,
            max_round=20,
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat, llm_config=self.base_config
        )
        manager.register_reply([autogen.Agent, None], self._on_reply)

        logger.info("Starting Crew")
        with Cache.disk() as cache:
            await self.user_proxy.a_initiate_chat(
                manager, message=message, cache=cast(Cache, cache), silent=True
            )

        await asyncio.sleep(1)

        if q and job_done:
            await q.put(job_done)
        else:
            logger.warning("No queue or job_done object provided")
