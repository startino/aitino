from typing import Any

from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    """Data model for LLM Config for AutoGen"""

    config_list: list[Any] = Field(default=[])
    temperature: float = 0
    cache_seed: int
    timeout: int | None = None
    max_tokens: int | None = None
