from typing import Any, Literal

from pydantic import BaseModel


class APIReply(BaseModel):
    id: int
    status: Literal["success"] | Literal["error"] = "success"
    data: Any
