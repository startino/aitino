from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Tool(BaseModel):
    id: UUID
    created_at: datetime
    name: str
    description: str
    api_key_type_id: UUID | None = None


class ToolInsertRequest(BaseModel):
    name: str
    description: str
    api_key_type_id: UUID | None = None


class ToolUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    api_key_type_id: UUID | None = None


class ToolGetRequest(BaseModel):
    name: str | None = None
    api_key_type_id: UUID | None = None