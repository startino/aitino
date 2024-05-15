import logging
import os
import re
from typing import Annotated, Any, Callable, cast
from uuid import UUID

import autogen
import tiktoken
from autogen.agentchat.contrib.retrieve_user_proxy_agent import (
    RetrieveUserProxyAgent,
)
from autogen.agentchat.utils import gather_usage_summary
from autogen.cache import Cache
from autogen.function_utils import get_function_schema
from fastapi import HTTPException
from langchain.tools import BaseTool

from src.interfaces import db
from src.models import (
    Agent,
    CodeExecutionConfig,
    CrewProcessed,
    Message,
    RagOptions,
    Session,
)
from src.models.session import SessionStatus
from src.tools import (
    generate_llm_config,
    generate_tool_from_uuid,
    get_tool_ids_from_agent,
)


class RagContext:
    def __init__(
        self,
        task: str | None,
        docs_path: str | list[str] | None,
    ):
        self.task = task
        self.docs_path = docs_path
        self.proxy = RetrieveUserProxyAgent(
            name="Boss_Assistant",
            is_termination_msg=lambda x: x.get("content", "")
            .rstrip()
            .endswith("TERMINATE"),
            system_message="Assistant who has extra content retrieval power for solving difficult problems.",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=3,
            retrieve_config={
                "task": self.task,
                "docs_path": self.docs_path,
                "get_or_create": True,
                "model": "gpt-3.5-turbo",
            },
            code_execution_config=False,  # we don't want to execute code in this case.
        )

    @classmethod
    def get_default(cls):
        return RagContext(task="default", docs_path=None)


ACCURACY = os.environ.get("MONETARY_DECIMAL_ACCURACY")
if ACCURACY is None:
    raise ValueError("MONETARY_DECIMAL_ACCURACY environment variable not set")


class AutogenCrew:
    def __init__(
        self,
        profile_id: UUID,
        session: Session,
        crew_model: CrewProcessed,
        rag_options: RagOptions,
        on_message: Any | None = None,
        base_model: str = "gpt-4-turbo",
        seed: int = 42,
    ):
        self.seed = seed
        self.profile_id = profile_id
        self.profile = db.get_profile(profile_id)
        self.session = session
        self.on_reply = on_message
        self.crew_model = crew_model
        self.valid_tools: list[BaseTool] = []
        self.rag_options = rag_options
        self.agents: list[autogen.ConversableAgent | autogen.Agent] = (
            self._create_agents(crew_model)
        )
        self.user_proxy = autogen.UserProxyAgent(
            name="Admin",
            max_consecutive_auto_reply=2,
            is_termination_msg=lambda x: x.get("content", "")
            .rstrip()
            .endswith("TERMINATE"),
            human_input_mode="NEVER",
            default_auto_reply="TERMINATE",
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
        wrapped_function = self.user_proxy._wrap_function(self._retrieve_content)
        self.user_proxy.register_function({"retrieve_content": wrapped_function})

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
        if rag_options.use_rag:
            self.rag = RagContext(
                task=rag_options.task, docs_path=rag_options.docs_path
            )
        else:
            self.rag = RagContext.get_default()

        if not self.profile:
            raise HTTPException(
                404,
                "profile not found",
            )
        self.funds = self.profile.funding
        if self.funds <= 0:
            raise HTTPException(
                402,
                "Insufficient funds",
            )

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

    def register_func_to_config(
        self,
        name: str,
        description: str,
        function: Callable[..., Any],
        agent: autogen.AssistantAgent,
    ):
        function_schema = get_function_schema(
            function, name=name, description=description
        )
        agent.update_tool_signature(
            function_schema,
            is_remove=False,
        )

        return function

    def _retrieve_content(
        self,
        message: Annotated[
            str,
            "Refined message which keeps the original meaning and can be used to retrieve content for code generation and question answering.",
        ],
        n_results: Annotated[int, "number of results"] = 3,
    ) -> str:
        """
        This function retrieves content based on a given message and a specified number of results.

        Parameters:
        message (str): A refined message which keeps the original meaning and can be used to retrieve content for code generation and question answering.
        n_results (int): The number of results to retrieve. Default is 3.

        Returns:
        str: The retrieved content. If no content is retrieved, the original message is returned.

        """
        # Check if we need to update the context.
        update_context_case1, update_context_case2 = (
            self.rag.proxy._check_update_context(message)
        )
        # If either context update case is true and the self.rag.proxy's update_context attribute is also true
        if (
            update_context_case1 or update_context_case2
        ) and self.rag.proxy.update_context:
            # Update the problem attribute of self.rag.proxy with the message if it doesn't already exist
            self.rag.proxy.problem = (  # type: ignore
                message
                if not hasattr(self.rag.proxy, "problem")
                else self.rag.proxy.problem  # type: ignore
            )
            # Generate a user reply based on the message
            _, ret_msg = self.rag.proxy._generate_retrieve_user_reply(message)  # type: ignore
        else:
            # If the context doesn't need to be updated, create a context dictionary with the problem and number of results
            _context = {"problem": message, "n_results": n_results}
            # Generate a message based on the context
            ret_msg = self.rag.proxy.message_generator(self.rag.proxy, None, _context)
        # Return the retrieved message if it exists, otherwise return the original message
        return ret_msg if ret_msg else message  # type: ignore

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

            system_message = f"""{agent.role}\n\n{agent.system_message}. If you write a program, give the program to the admin. End the message with the agent you want to speak to."""

            agent_instance = autogen.AssistantAgent(
                name=self._format_agent_name(agent),
                system_message=system_message,
                description=agent.description,
                llm_config=config,
            )
            if agent.id == crew_model.receiver_id:
                agent_instance.update_system_message(
                    system_message
                    + "\nReply 'Admin' if all tasks has been solved at full satisfaction."
                )
            if self.on_reply:
                agent_instance.register_reply([autogen.Agent, None], self._on_reply)

            if self.rag_options.use_rag:
                self.decorated_function = self.register_func_to_config(
                    name="retrieve_content",
                    description="retrieve content for code generation and question answering.",
                    function=self._retrieve_content,
                    agent=agent_instance,
                )
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
            return round(cost * int(ACCURACY) * 1.05)

        return int(cost * int(ACCURACY) * 1.05)

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
        chat_agents = self.agents + [self.user_proxy]
        if self.rag_options.use_rag:
            chat_agents.append(self.rag.proxy)

        logging.info(f"agents: {chat_agents}")
        groupchat = autogen.GroupChat(
            agents=chat_agents,
            messages=dict_messages,
            max_round=30,
            speaker_selection_method="auto",
            # TODO: Fix auto method to not spam route to admin
            send_introductions=True,
            select_speaker_message_template="""You are in a role play game. The following roles are available:
                {roles}.
                Read the following conversation.
                Then select the next role from {agentlist} to play. Only return the role. Select admin if the task is done or to execute code or to use a tool""",
            select_speaker_prompt_template="""Read the above conversation. 
                Then select the next role from {agentlist} to play. Only return the role. Select admin if the task is done or to execute code or to use a tool""",
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat,
            llm_config=self.base_config,
        )
        manager.register_reply([autogen.Agent, None], self._on_reply)
        logging.info("Starting Crew")
        with Cache.disk() as cache:
            logging.info("Starting chat")
            chat_result = await self.user_proxy.a_initiate_chat(
                manager, message=message, cache=cast(Cache, cache), max_turns=10
            )

        logging.info(f"chat result: {chat_result}")

        manager_admin_cost = chat_result.cost["usage_excluding_cached_inference"][
            "total_cost"
        ]
        agent_cost_dict = gather_usage_summary(groupchat.agents)
        agent_cost = agent_cost_dict["usage_excluding_cached_inference"]["total_cost"]

        logging.info(f"manager + admin cost: {manager_admin_cost}")
        logging.info(f"agent cost: {agent_cost}")
        total_cost = manager_admin_cost + agent_cost

        logging.info(f"Cost: {total_cost}")
        new_funding = self.funds - self.add_margin(total_cost)  # type: ignore
        logging.info(
            f"New funding: {new_funding}, cost with margin: {self.add_margin(total_cost)}"
        )

        db.update_funding(self.profile_id, new_funding)

        db.update_status(self.session.id, SessionStatus.FINISHED)
