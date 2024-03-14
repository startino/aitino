import logging
from asyncio import Queue
from typing import Any, cast
from uuid import UUID, uuid4

import autogen
from autogen.cache import Cache

from .interfaces import db
from .models import CodeExecutionConfig, CrewModel, Message, Session

logger = logging.getLogger("root")


class Crew:
    def __init__(
        self,
        profile_id: UUID,
        session: Session,
        crew_model: CrewModel,
        on_message: Any | None = None,
        base_model: str = "gpt-4-turbo-preview",
        seed: int = 41,
    ):
        self.seed = seed
        self.profile_id = profile_id
        self.session = session
        self.on_reply = on_message
        if not self._validate_crew_model(crew_model):
            raise ValueError("composition is invalid")
        self.crew_model = crew_model

        self.user_proxy = autogen.UserProxyAgent(
            name="Admin",
            system_message="""Reply TERMINATE if the task has been solved at full satisfaction. If you instead require more information reply TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
            max_consecutive_auto_reply=4,
            human_input_mode="NEVER",
            default_auto_reply="Reply TERMINATE if the task has been solved at full satisfaction. If you instead require more information reply TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.",
            code_execution_config=CodeExecutionConfig(
                work_dir=f".cache/{self.seed}/scripts"
            ).model_dump(),
        )

        self.agents: list[autogen.ConversableAgent | autogen.Agent] = (
            self._create_agents(crew_model)
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
        # This function is called when an LLM model replies
        if not self.on_reply:
            logger.warn("No on_reply function")
            return False, None

        logger.debug(f"on_reply: {recipient.name} {messages}")

        if not messages:
            logger.error("on_reply: No messages")
            return False, None
        if len(messages) == 0:
            logger.error("on_reply: No messages")
            return False, None

        last_msg = messages[-1]

        # Validate last message
        if not last_msg.get("name"):
            logger.warn(f"on_reply: No name\n{last_msg}")
            last_msg["name"] = (
                "None"  # changed from None to "None" which helped fix the error 'message': "None is not of type 'string' but felt like it made the chat manager worse
            )
        if not last_msg.get("content"):
            logger.error(f"on_reply: No content\n{last_msg}")
            return False, None
        if not last_msg.get("role"):
            logger.error(f"on_reply: No role\n{last_msg}")
            return False, None

        name = last_msg["name"]
        content = last_msg["content"]
        role = last_msg["role"]
        recipient_id = None  # None means admin
        sender_id = None  # None means admin

        for agent in self.crew_model.agents:
            check_name = (
                f"""{agent.title.replace(' ', '')}-{agent.title.replace(' ', '')}"""
            )
            if check_name == recipient.name:
                recipient_id = agent.id
            if check_name == name:
                sender_id = agent.id

        if (
            recipient_id is None
            and sender_id is None
            and recipient.name != "chat_manager"
        ):
            logger.warn(
                "on_reply: Both recipient and sender are None (admin) or chat_manager"
            )
            return False, None
        logger.warn(
            f"_on_reply: name: {name}\ncontent: {content}\n role:{role}\nrecipient_id: {recipient_id}\nsender_id: {sender_id}"
        )
        await self.on_reply(recipient_id, sender_id, content, role)

        return False, None

    def _validate_crew_model(self, crew_model: CrewModel) -> bool:
        if len(crew_model.agents) == 0:
            return False

        # Validate agents
        for agent in crew_model.agents:
            if agent.title == "":
                return False
            if agent.title == "":
                return False
            if agent.system_message == "":
                return False
        return True

    def _create_agents(
        self, crew_model: CrewModel
    ) -> list[autogen.ConversableAgent | autogen.Agent]:
        agents = []
        descriptions = db.get_descriptions([agent.id for agent in crew_model.agents])
        if not descriptions:
            raise ValueError("at least one agent id is invalid")

        for agent in crew_model.agents:
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

            agent_instance = autogen.AssistantAgent(
                name=f"""{agent.title.replace(' ', '')}-{agent.title.replace(' ', '')}""",  # TODO: make failsafes to make sure this name doesn't exceed 64 chars - Leon
                system_message=f"""{agent.title}\n\n{agent.system_message}. Additionally, if information from the internet is required for completing the task, write a program to search the
                internet for what you need and only output this program. If your program requires imports, add a sh script at the top of your output to install these packages.
                Give this program to the admin. """,  # TODO: add what agent it should send to next - Leon
                description=descriptions[agent.id][0],  # could add something to concatenate all strings in description list for a given agent - Leon
                llm_config=config,
            )
            if agent.id == crew_model.receiver_id:
                agent_instance.update_system_message(
                    f"""{agent.title}\n\n{agent.system_message}. Write TERMINATE if all tasks has been solved at full satisfaction. If you instead require more information write TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the tasks are not solved yet."""
                )
            if self.on_reply:
                agent_instance.register_reply([autogen.Agent, None], self._on_reply)
            agents.append(agent_instance)

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
            send_introductions=True,
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat, llm_config=self.base_config
        )
        manager.register_reply([autogen.Agent, None], self._on_reply)

        logger.info("Starting Crew")
        with Cache.disk() as cache:
            logger.info("Starting chat")
            await self.user_proxy.a_initiate_chat(
                manager, message=message, cache=cast(Cache, cache)
            )
