import autogen

from .parser import Composition


class Maeve:
    def __init__(
        self, composition: Composition, base_model: str = "gpt-4-turbo-preview"
    ):
        if not self.validate_composition(composition):
            raise ValueError("composition is invalid")

        self.user_proxy = autogen.UserProxyAgent(
            name="Admin",
            system_message="A human admin and code executor.",
            max_consecutive_auto_reply=1,
            human_input_mode="NEVER",
            code_execution_config={
                "last_n_messages": 4,
                "work_dir": "tasks",
                "use_docker": False,
            },
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
            "cache_seed": 41,
            "temperature": 0,
            "config_list": self.base_config_list,
            "timeout": 120,
        }

    def validate_composition(self, composition: Composition):
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
                "cache_seed": 41,
                "temperature": 0,
                "config_list": config_list,
                "timeout": 120,
            }

            agents.append(
                autogen.AssistantAgent(
                    name=f"""{agent.job_title.replace(' ', '')}-{agent.name.replace(' ', '')}""",
                    system_message=f"""{agent.job_title} {agent.name}. {agent.system_message}. Stick to your role, do not do something yourself which another team member can do better.""",
                    llm_config=config,
                )
            )
        return agents

    def run(self, message: str):
        groupchat = autogen.GroupChat(
            agents=self.agents + [self.user_proxy],
            messages=[],
            max_round=20,
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat, llm_config=self.base_config
        )

        result = self.user_proxy.initiate_chat(
            manager,
            message=message,
        )
        return result
