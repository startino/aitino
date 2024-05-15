from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Tool(BaseModel):
    id: UUID
    created_at: datetime
    name: str
    description: str
    api_provider_id: UUID | None = None


class ToolInsertRequest(BaseModel):
    name: str
    description: str
    api_provider_id: UUID | None = None


class ToolUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    api_provider_id: UUID | None = None


class ToolGetRequest(BaseModel):
    name: str | None = None
    api_provider_id: UUID | None = None
