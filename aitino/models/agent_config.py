from typing import Callable, Literal
from uuid import UUID

from pydantic import BaseModel, Field

from .llm_config import LLMConfig
from .code_execution_config import CodeExecutionConfig


class AgentConfig(BaseModel):
    """Data model for Agent Config for AutoGen"""

    id: UUID
    name: str
    role: str
    system_message: str
    llm_config: LLMConfig
    human_input_mode: str = "NEVER"
    max_consecutive_auto_reply: int = 10
    is_termination_msg: bool | str | Callable = Field(
        default=lambda msg: "TERMINATE" in msg.get("content", "")
    )
    code_execution_config: CodeExecutionConfig | Literal[False] = False
    default_auto_reply: str = "Reply `TERMINATE` if the task is done."
