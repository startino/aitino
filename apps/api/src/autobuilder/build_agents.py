import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import autogen


logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    model: str = "gpt-4-turbo"
    seed: int = 41
    temperature: float = 0.0
    timeout: int = 120


@dataclass
class TeamSpec:
    simplified_task: str
    team_description: str


class BuildAgents:
    def __init__(self, config: Optional[AgentConfig] = None) -> None:
        self._config = config or AgentConfig()
        self._llm_config: Optional[dict] = None

    def _get_llm_config(self) -> dict:
        if self._llm_config is None:
            config_list = autogen.config_list_from_json(
                "OAI_CONFIG_LIST",
                filter_dict={"model": [self._config.model]},
            )
            self._llm_config = {
                "seed": self._config.seed,
                "temperature": self._config.temperature,
                "config_list": config_list,
                "timeout": self._config.timeout,
            }
        return self._llm_config

    def _load_prompt(self, filename: str) -> str:
        path = Path(os.getcwd(), "src", "prompts", "autobuild", filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def create_task_simplifier(self) -> autogen.ConversableAgent:
        return autogen.ConversableAgent(
            name="tasksimplifier-testagent",
            system_message=self._load_prompt("task_simplifier.md"),
            llm_config=self._get_llm_config(),
        )

    def create_employer(self) -> autogen.ConversableAgent:
        return autogen.ConversableAgent(
            name="agentemployer-testagent",
            system_message=self._load_prompt("create-employer.md"),
            llm_config=self._get_llm_config(),
        )

    def create_all_in_one_agent(self) -> autogen.AssistantAgent:
        return autogen.AssistantAgent(
            name="teamspecialist",
            system_message=self._load_prompt("team-specialist.md"),
            llm_config=self._get_llm_config(),
        )


class AutobuildPipeline:
    """Orchestrates the full agent pipeline: simplify a task, then produce a team spec."""

    def __init__(
        self,
        agent_config: Optional[AgentConfig] = None,
        max_simplify_turns: int = 2,
        max_team_turns: int = 3,
    ) -> None:
        self._builder = BuildAgents(config=agent_config)
        self._max_simplify_turns = max_simplify_turns
        self._max_team_turns = max_team_turns

    def _make_proxy(self) -> autogen.UserProxyAgent:
        return autogen.UserProxyAgent(
            name="proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            code_execution_config=False,
        )

    @staticmethod
    def _last_assistant_reply(chat_result: autogen.ChatResult) -> str:
        for msg in reversed(chat_result.chat_history):
            if msg.get("role") == "assistant":
                return msg.get("content", "")
        return ""

    def simplify_task(self, task: str) -> str:
        proxy = self._make_proxy()
        result = proxy.initiate_chat(
            self._builder.create_task_simplifier(),
            message=task,
            max_turns=self._max_simplify_turns,
        )
        reply = self._last_assistant_reply(result)
        logger.debug("simplified task: %.120s", reply)
        return reply or task

    def build_team_spec(self, simplified_task: str) -> str:
        proxy = self._make_proxy()
        result = proxy.initiate_chat(
            self._builder.create_all_in_one_agent(),
            message=simplified_task,
            max_turns=self._max_team_turns,
        )
        reply = self._last_assistant_reply(result)
        logger.debug("team spec: %.120s", reply)
        return reply

    def run(self, task: str) -> TeamSpec:
        """Run the full pipeline and return a TeamSpec.

        Simplifies the raw task first, then asks the team specialist to produce
        an agent team description. Raises RuntimeError if either step returns empty.
        """
        logger.info("autobuild pipeline started: %.80s", task)

        simplified = self.simplify_task(task)
        if not simplified:
            raise RuntimeError("task simplifier returned an empty response")

        team_description = self.build_team_spec(simplified)
        if not team_description:
            raise RuntimeError("team specialist returned an empty response")

        logger.info("autobuild pipeline complete")
        return TeamSpec(simplified_task=simplified, team_description=team_description)
