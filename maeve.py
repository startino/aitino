from typing import List, Union

import autogen


class Maeve:
    def __init__(self, base_model, composition):
        self.validate_composition(composition)

        self.user_proxy = autogen.UserProxyAgent(
            name="Admin",
            system_message="A human admin.",
            code_execution_config=False,
        )

        self.agents: List[Union[autogen.ConversableAgent, autogen.Agent]] = (
            self.create_agents(composition)
        )

        self.base_config_list = autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": [base_model],
            },
        )
        self.base_config = {
            "cache_seed": 41,
            "temperature": 0,
            "config_list": self.base_config_list,
            "timeout": 120,
        }

    def validate_composition(self, composition):
        for group in composition:
            if len(group) < 2:
                print("Each group must have at least two agents.")
                return False
        return True

    def create_agents(
        self, composition
    ) -> List[Union[autogen.ConversableAgent, autogen.Agent]]:
        agents = []

        for agent in composition:
            config_list = autogen.config_list_from_json(
                "OAI_CONFIG_LIST",
                filter_dict={
                    "model": [agent["model"]],
                },
            )

            config = {
                "cache_seed": 41,
                "temperature": 0,
                "config_list": config_list,
                "timeout": 120,
            }

            agents.append(
                autogen.AssistantAgent(
                    name=agent["name"],
                    system_message=agent["system_message"],
                    llm_config=config,
                )
            )
        return agents

    def run(self, message):
        groupchat = autogen.GroupChat(
            agents=self.agents + [self.user_proxy],
            messages=[],
            max_round=50,
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat, llm_config=self.base_config
        )

        self.user_proxy.initiate_chat(
            manager,
            message=message,
        )
