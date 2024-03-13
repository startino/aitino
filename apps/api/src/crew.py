import asyncio
import logging
from asyncio import Queue
from typing import Any, cast
from uuid import UUID, uuid4

import autogen
from autogen.cache import Cache
from pydantic import BaseModel, Field

from .interfaces import db
from .models import CodeExecutionConfig, CrewModel, Message, Session

logger = logging.getLogger("root")


class Crew:
    def __init__(
        self,
        profile_id: UUID,
        session: Session,
        composition: CrewModel,
        on_message: Any | None = None,
        base_model: str = "gpt-4-turbo-preview",
        seed: int = 41,
    ):
        self.seed = seed
        self.profile_id = profile_id
        self.session = session
        self.on_reply = on_message
        if not self._validate_composition(composition):
            raise ValueError("composition is invalid")
        self.composition = composition

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
            self._create_agents(composition)
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
        sender: autogen.Agent | None = None,
        config: Any | None = None,
    ) -> tuple[bool, Any | None]:
        if self.on_reply:
            await self.on_reply(recipient, messages, sender, config)
        else:
            logger.warn("No on_reply function")

        return False, None

    def _validate_composition(self, composition: CrewModel) -> bool:
        if len(composition.agents) == 0:
            return False

        # Validate agents
        for agent in composition.agents:
            if agent.role == "":
                return False
            if agent.title == "":
                return False
            if agent.system_message == "":
                return False
        return True

    def _create_agents(
        self, composition: CrewModel
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
                name=f"""{agent.role.replace(' ', '')}-{agent.title.replace(' ', '')}""",
                system_message=f"""{agent.role} {agent.title}. {agent.system_message}. Reply TERMINATE if the task has been solved at full satisfaction. If you instead require more information reply TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
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
    ) -> None:
        logger.debug("Running Crew")

        # convert Message list to dict list
        dict_messages = [m.model_dump() for m in (messages if messages else [])]

        groupchat = autogen.GroupChat(
            agents=self.agents + [self.user_proxy],
            messages=dict_messages,
            max_round=20,
            speaker_selection_method="auto" if len(self.agents) > 1 else "round_robin",
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat, llm_config=self.base_config
        )
        manager.register_reply([autogen.Agent, None], self._on_reply)

        logger.info("Starting Crew")
        with Cache.disk() as cache:
            logger.info("Starting chat")
            result = await self.user_proxy.a_initiate_chat(
                manager, message=message, cache=cast(Cache, cache)
            )

        raw_msg = result.chat_history[-1]

        sender_id = None
        for agent in self.composition.agents:
            if (
                f"""{agent.role.replace(' ', '')}-{agent.title.replace(' ', '')}"""
                == raw_msg["name"]
            ):
                sender_id = agent.id

        last_message = Message(
            session_id=self.session.id,
            profile_id=self.profile_id,
            recipient_id=None,
            sender_id=sender_id,
            content=raw_msg["content"],
            role=raw_msg["role"],
        )
        db.post_message(last_message)

        logger.info("Chat finished")

        logger.info("Crew finished")
        await asyncio.sleep(1)
