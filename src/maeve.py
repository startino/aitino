from autogen.graph_utils import visualize_speaker_transitions_dict

import autogen


class Maeve:
    def __init__(self, base_model, composition):
        self.validate_composition(composition)

        self.user_proxy = autogen.UserProxyAgent(
            name="Admin",
            system_message="A human admin and code executor.",
            code_execution_config={
                "last_n_messages": 4,
                "work_dir": "tasks",
                "use_docker": True,
            },
        )

        self.agents: list[
            autogen.ConversableAgent | autogen.Agent
        ] = self.create_agents(composition)

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

        self.speaker_transitions_dict = {}

    def validate_composition(self, composition):
        for group in composition:
            if len(group) < 2:
                print("Each group must have at least two agents.")
                return False
        return True

    def create_agents(
        self, composition
    ) -> list[autogen.ConversableAgent | autogen.Agent]:
        agents = []

        for agent in composition["agents"]:
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
                    name=f"""{agent["job_title"].replace(' ', '')}-{agent["name"].replace(' ', '')}""",
                    system_message=f"""{agent["job_title"]} {agent["name"]}. {agent["system_message"]}. Stick to your role, do not do something yourself which another team member can do better.""",
                    llm_config=config,
                )
            )
        return agents

    def graph(self):
        groupchat = autogen.GroupChat(
            agents=self.agents + [self.user_proxy],
            messages=[],
            max_round=50,
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat, llm_config=self.base_config
        )

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
