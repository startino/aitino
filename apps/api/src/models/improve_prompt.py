from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class ImproveInsertRequest(BaseModel):
    prompt: str
    word_limit: int
    prompt_type: Literal["generic", "system", "user"]
    profile_id: UUID
    temperature: float
