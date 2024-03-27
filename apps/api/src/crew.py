import logging
import re
from typing import Any, cast
from uuid import UUID

import autogen
from autogen.cache import Cache

from src.models.session import SessionStatus

from .interfaces import db
from .models import AgentModel, CodeExecutionConfig, CrewModel, Message, Session
from .tools import (
    generate_llm_config,
    generate_tool_from_uuid,
    get_tool_ids_from_agent,
)

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
        self.valid_tools = []

        self.agents: list[autogen.ConversableAgent | autogen.Agent] = (
            self._create_agents(crew_model)
        )

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
        (
            self.user_proxy.register_function(
                # ternary operator evaluates if there are any tools in valid_tools and calls register_function if there are valid tools.
                function_map={tool.name: tool._run for tool in self.valid_tools}
            )
            if self.valid_tools
            else None
        )
        self.user_proxy.register_reply([autogen.Agent, None], self._on_reply)

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
            last_msg["name"] = None
        if not last_msg.get("content"):
            logger.error(f"on_reply: No content\n{last_msg}")
            return False, None
        if not last_msg.get("role"):
            logger.error(f"on_reply: No role\n{last_msg}")
            return False, None

        sender_name = last_msg["name"]
        content = last_msg["content"]
        role = last_msg["role"]
        recipient_id = None  # None means admin
        sender_id = None  # None means admin

        for agent in self.crew_model.agents:
            check_name = self._format_agent_name(agent)
            if check_name == recipient.name:
                recipient_id = agent.id
            if check_name == sender_name:
                sender_id = agent.id

        # checks if all of the fields are false
        if not any(
            [
                recipient_id,
                sender_id,
                sender_name == "Admin",
                recipient.name == "chat_manager",
            ]
        ):
            logger.warn(
                f"on_reply: both ids are none, sender is not admin and recipient is not chat manager"
            )

        await self.on_reply(recipient_id, sender_id, content, role)
        return False, None

    def _validate_crew_model(self, crew_model: CrewModel) -> bool:
        if len(crew_model.agents) == 0:
            return False

        # Validate agents
        for agent in crew_model.agents:
            if agent.role == "":
                return False
            if agent.title == "":
                return False
            if agent.system_message == "":
                return False
        return True

    def _extract_uuid(self, dictionary: dict[UUID, list[str]]) -> dict[UUID, list[str]]:
        new_dict = {}
        for key, value in dictionary.items():
            if isinstance(key, UUID):
                logger.warn("went through isinstance if statement!")
                new_dict[key] = value

            try:
                split_uuid = str(key).split("(")
                logger.warn(f"split_uuid: {split_uuid}")
                new_dict[UUID(split_uuid[0])] = value
            except ValueError:
                # if the key can't be converted to uuid, return the old value
                new_dict[key] = value
        return new_dict

    def _format_agent_name(self, agent: AgentModel) -> str:
        return re.sub(
            r"[^a-zA-Z0-9-]",
            "",
            f"""{agent.role.replace(' ', '')}-{agent.role.replace(' ', '')}""",
        )[:64]

    def _create_agents(
        self, crew_model: CrewModel
    ) -> list[autogen.ConversableAgent | autogen.Agent]:
        agents = []
        descriptions = db.get_descriptions([agent.id for agent in crew_model.agents])
        if not descriptions:
            raise ValueError("at least one agent id is invalid")

        formatted_descriptions = self._extract_uuid(descriptions)
        # idk why this is the only way i got it working, but will hopefully simplify later...
        # this function basically takes a uuid and turns it into uuid again, but the program stopped throwing key errors when i use this formatted_description

        profile_api_keys = db.get_tool_api_keys(self.profile_id)

        for agent in crew_model.agents:
            valid_agent_tools = []
            tool_schemas = {}
            config_list = autogen.config_list_from_json(
                "OAI_CONFIG_LIST",
                filter_dict={
                    "model": [agent.model],
                },
            )
            tool_ids = get_tool_ids_from_agent(agent.tools)
            api_key_types = db.get_api_key_type_ids(tool_ids)

            # db.get_tool_api_keys(self.profile_id, list(api_key_types.values()))
            if len(tool_ids):
                for tool in tool_ids:
                    try:
                        generated_tool = generate_tool_from_uuid(tool, api_key_types, profile_api_keys)
                    except TypeError as e:
                        raise e
                    ((self.valid_tools.append(generated_tool), valid_agent_tools.append(generated_tool)) if generated_tool is not None else None)

                logger.warn(f"{self.valid_tools=}")
                tool_schemas = (
                    generate_llm_config(valid_agent_tools)
                    if valid_agent_tools
                    else None
                )

            logger.warn(
                f"agent tools: {agent.tools}, valid agent tools: {valid_agent_tools=}, valid tools: {self.valid_tools}"
            )
            config = {
                "seed": self.seed,
                "temperature": 0,
                "config_list": config_list,
                "timeout": 120,
            }
            if tool_schemas:
                config["functions"] = tool_schemas

            system_message = f"""{agent.role}\n\n{agent.system_message}. If you write a program, give the program to the admin. """  # TODO: add what agent it should send to next - Leon

            agent_instance = autogen.AssistantAgent(
                name=self._format_agent_name(agent),
                system_message=system_message,
                description=formatted_descriptions[agent.id][0],
                # could add something to concatenate all strings in description list for a given agent - Leon
                llm_config=config,
            )
            if agent.id == crew_model.receiver_id:
                agent_instance.update_system_message(
                    system_message
                    + "\nWrite TERMINATE if all tasks has been solved at full satisfaction. If you instead require more information write TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the tasks are not solved yet."
                    ""
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
        speaker_selection_method = "auto" if len(self.agents) > 1 else "round_robin"
        logger.info(speaker_selection_method)
        groupchat = autogen.GroupChat(
            agents=self.agents + [self.user_proxy],
            messages=dict_messages,
            max_round=20,
            speaker_selection_method="round_robin",
            # TODO: Fix auto method to not spam route to admin
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
        db.update_status(self.session.id, SessionStatus.FINISHED)
