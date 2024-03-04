from typing import Callable, Literal
from uuid import UUID

from pydantic import BaseModel, Field

from .code_execution_config import CodeExecutionConfig
from .llm_config import LLMConfig


class AgentConfig(BaseModel):
    """Data model for Agent Config for AutoGen"""

    id: UUID
    name: str
    role: str
    system_message: str
    human_input_mode: str = "NEVER"
    max_consecutive_auto_reply: int = 10
    is_termination_msg: bool | str | Callable = Field(
        default=lambda msg: "TERMINATE" in msg.get("content", "")
    )
    llm_config: LLMConfig | Literal[False] = False
    code_execution_config: CodeExecutionConfig | Literal[False] = False
    default_auto_reply: str = (
        "Reply TERMINATE if the task has been solved at full satisfaction. If you instead require more information reply TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the task is not solved yet."
    )
