from autogen import UserProxyAgent
from .ret_conversable_agent import RetConversableAgent


class RetUserProxyAgent(UserProxyAgent, RetConversableAgent):
    pass
