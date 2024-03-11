import os
from pathlib import Path

import autogen


class BuildAgents:
    def create_task_simplifier(self) -> autogen.ConversableAgent:
        config_list = autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": ["gpt-4-turbo-preview"],
            },
        )
        config = {
            "seed": 41,
            "temperature": 0.0,
            "config_list": config_list,
            "timeout": 120,
        }
        with open(
            Path(os.getcwd(), "src", "prompts", "autobuild", "task_simplifier.md"),
            "r",
            encoding="utf-8",
        ) as f:
            system_prompt = f.read()
            return autogen.ConversableAgent(
                name="""tasksimplifier-testagent""",
                system_message=system_prompt,
                llm_config=config,
            )

    def create_employer(self) -> autogen.ConversableAgent:
        config_list = autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": ["gpt-4-turbo-preview"],
            },
        )
        config = {
            "seed": 41,
            "temperature": 0.0,
            "config_list": config_list,
            "timeout": 120,
        }
        with open(
            Path(os.getcwd(), "src", "prompts", "autobuild", "create-employer.md"),
            "r",
            encoding="utf-8",
        ) as f:
            system_prompt = f.read()
            return autogen.ConversableAgent(
                name="""agentemployer-testagent""",
                system_message=system_prompt,
                llm_config=config,
            )

    def create_all_in_one_agent(self) -> autogen.AssistantAgent:
        config_list = autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": ["gpt-4-turbo-preview"],
            },
        )

        config = {
            "seed": 41,
            "temperature": 0.0,
            "config_list": config_list,
            "timeout": 120,
        }

        with open(
            Path(os.getcwd(), "src", "prompts", "autobuild", "team-specialist.md"),
            "r",
            encoding="utf-8",
        ) as f:
            system_prompt = f.read()
            return autogen.AssistantAgent(
                name="""teamspecialist""",
                system_message=system_prompt,
                # should add something to parse a list of good agents from the database, give them to this agent and give those agents as examples for it to use during team creation
                # should also add something that is better at dynamically making teams of agents that work together (my solution here is to tell it to make teams, which is not optimal)
                llm_config=config,
            )
