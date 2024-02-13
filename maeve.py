from typing import List

import autogen


class Maeve:
    def __init__(self, base_model, composition):
        self.agents = composition["agents"]
        self.generics = composition["generics"]
        self.groups = composition["groups"]
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

    def validate_composition(self):
        for group in self.groups:
            if len(group) < 2:
                print("Each group must have at least two agents.")
                return False
        return True

    def get_generic(self, generic_id):
        return next((item for item in self.generics if item["id"] == generic_id))

    def create_agents(self) -> List[autogen.Agent]:
        agents = []

        for agent in self.agents:
            generic = self.get_generic(agent["generic_id"])

            # config_list = autogen.config_list_from_json(
            #     "OAI_CONFIG_LIST",
            #     filter_dict={
            #         "model": [generic["model"]],
            #     },
            # )
            # config = {
            #     "cache_seed": 41,
            #     "temperature": 0,
            #     "config_list": config_list,
            #     "timeout": 120,
            # }
            agents.append(
                autogen.AssistantAgent(
                    name=agent["name"],
                    system_message=generic["system_message"],
                    llm_config=self.base_config,
                )
            )
        return agents

    def run(self, message):
        if not self.validate_composition():
            return

        user_proxy = autogen.UserProxyAgent(
            name="Admin",
            system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
            code_execution_config=False,
        )

        executor = autogen.UserProxyAgent(
            name="Executor",
            system_message="Executor. Execute the code written by the engineer and report the result.",
            human_input_mode="NEVER",
            code_execution_config={
                "last_n_messages": 3,
                "work_dir": "paper",
                "use_docker": True,
            },
        )

        agents: List[autogen.Agent] = self.create_agents()

        groupchat = autogen.GroupChat(
            agents=agents + [user_proxy, executor],
            messages=[],
            max_round=50,
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat, llm_config=self.base_config
        )

        user_proxy.initiate_chat(
            manager,
            message=message,
        )
