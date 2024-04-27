import logging
import re
from typing import Any, cast
from uuid import UUID
import tiktoken

import autogen
from autogen.cache import Cache
from fastapi import HTTPException
from langchain.tools import BaseTool

from src.interfaces import db
from src.models import (
    Agent,
    CodeExecutionConfig,
    CrewProcessed,
    Message,
    Session,
)
from src.models.session import SessionStatus
from src.tools import (
    generate_llm_config,
    generate_tool_from_uuid,
    get_tool_ids_from_agent,
)


class AutogenCrew:
    def __init__(
        self,
        profile_id: UUID,
        session: Session,
        crew_model: CrewProcessed,
        on_message: Any | None = None,
        base_model: str = "gpt-4-turbo",
        seed: int = 41,
    ):
        self.seed = seed
        self.profile_id = profile_id
        self.session = session
        self.on_reply = on_message
        self.crew_model = crew_model
        self.valid_tools: list[BaseTool] = []

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
            logging.warn("No on_reply function")
            return False, None

        logging.debug(f"on_reply: {recipient.name} {messages}")

        if not messages:
            logging.error("on_reply: No messages")
            return False, None
        if len(messages) == 0:
            logging.error("on_reply: No messages")
            return False, None

        last_msg = messages[-1]

        # Validate last message
        if not last_msg.get("name"):
            logging.warn(f"on_reply: No name\n{last_msg}")
            last_msg["name"] = None
        if not last_msg.get("content"):
            logging.error(f"on_reply: No content\n{last_msg}")
            return False, None
        if not last_msg.get("role"):
            logging.error(f"on_reply: No role\n{last_msg}")
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
            logging.error(
                "on_reply: both ids are none, sender is not admin and recipient is not chat manager"
            )

        await self.on_reply(recipient_id, sender_id, content, role)
        return False, None

    def _format_agent_name(self, agent: Agent) -> str:
        return re.sub(
            r"[^a-zA-Z0-9-]",
            "",
            f"""{agent.role.replace(' ', '')}-{agent.role.replace(' ', '')}""",
        )[:64]

    def _create_agents(
        self, crew_model: CrewProcessed
    ) -> list[autogen.ConversableAgent | autogen.Agent]:
        agents = []

        profile_api_keys = db.get_tool_api_keys(self.profile_id)

        for agent in crew_model.agents:
            config_list = autogen.config_list_from_json(
                "OAI_CONFIG_LIST",
                filter_dict={
                    "model": [agent.model],
                },
            )
            tool_ids = get_tool_ids_from_agent(agent.tools)
            api_key_types = db.get_api_provider_ids(tool_ids)

            # db.get_tool_api_keys(self.profile_id, list(api_key_types.values()))
            valid_agent_tools = []
            tool_schemas: list[dict] | None = []
            if len(tool_ids):
                for tool in tool_ids:
                    try:
                        generated_tool = generate_tool_from_uuid(
                            tool, api_key_types, profile_api_keys
                        )
                    except TypeError as e:
                        logging.error(f"tried to generate tool, got error: {e}")
                        raise HTTPException(
                            500, f"tried to generate tool, got error {e}"
                        )

                    (
                        (
                            self.valid_tools.append(generated_tool),
                            valid_agent_tools.append(generated_tool),
                        )
                        if generated_tool is not None
                        else None
                    )

                tool_schemas = (
                    generate_llm_config(valid_agent_tools)
                    if valid_agent_tools
                    else None
                )

            config = {
                "seed": self.seed,
                "temperature": 0,
                "config_list": config_list,
                "timeout": 120,
            }
            if tool_schemas:
                config["tools"] = tool_schemas

            system_message = f"""{agent.role}\n\n{agent.system_message}. If you write a program, give the program to the admin. """
            # TODO: add what agent it should send to next - Leon

            agent_instance = autogen.AssistantAgent(
                name=self._format_agent_name(agent),
                system_message=system_message,
                description=agent.description,
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

    def calculate_cost(self, chat_history: list[dict[str, str]]) -> float:
        input_list = []
        output_list = []
        # {"gpt-4-turbo": {"cost": 3, "input_tokens" : 0, "output_tokens": 0}}
        for messages in chat_history:
            input_list.append(messages.get("content"))
            if messages.get("role") == "assistant":
                output_list.append(messages.get("content"))

        # encoding for gpt-4 and gpt-3.5
        encoding = tiktoken.get_encoding("cl100k_base")
        all_input_messages = " ".join(input_list)
        all_output_messages = " ".join(output_list)
        input_tokens = encoding.encode(all_input_messages)
        output_tokens = encoding.encode(all_output_messages)

        input_cost = len(input_tokens) * 0.00001
        output_cost = len(output_tokens) * 0.00003
        return input_cost + output_cost

    def add_margin(self, cost: float) -> int:
        str_cost = str(cost)
        _, _, decimal_part = str_cost.partition(".")
        decimal_amount = len(decimal_part)

        if decimal_amount > 2:
            return round(cost * 100 * 1.05)

        return int(cost * 100 * 1.05)

    async def run(
        self,
        message: str,
        messages: list[Message] | None = None,
    ) -> None:
        logging.debug("Running Crew")

        # convert Message list to dict list
        dict_messages = [m.model_dump() for m in (messages if messages else [])]
        speaker_selection_method = "auto" if len(self.agents) > 1 else "round_robin"
        logging.info(speaker_selection_method)
        groupchat = autogen.GroupChat(
            agents=self.agents + [self.user_proxy],
            messages=dict_messages,
            max_round=100,
            speaker_selection_method="round_robin",
            # TODO: Fix auto method to not spam route to admin
            send_introductions=True,
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat, llm_config=self.base_config
        )
        manager.register_reply([autogen.Agent, None], self._on_reply)

        logging.info("Starting Crew")
        with Cache.disk() as cache:
            logging.info("Starting chat")
            chat_result = await self.user_proxy.a_initiate_chat(
                manager, message=message, cache=cast(Cache, cache)
            )

        logging.info(f"chat result: {chat_result}")

        total_cost = chat_result.cost["usage_including_cached_inference"]["total_cost"]

        logging.info(f"Cost: {total_cost}")
        profile = db.get_profile(self.profile_id)
        if not profile:
            raise HTTPException(
                500,
                "profile not found somehow, this is very weird and should not happen",
            )
        profile_funds = profile.funding
        new_funding = profile_funds - self.add_margin(total_cost + 0.01)  # type: ignore
        db.update_funding(self.profile_id, new_funding)

        db.update_status(self.session.id, SessionStatus.FINISHED)
