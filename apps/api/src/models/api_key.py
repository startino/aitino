from __future__ import annotations
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel


class APIKey(BaseModel):
    id: UUID
    created_at: datetime
    profile_id: UUID
    api_key_type: APIKeyType | None = None
    api_key: str


class APIKeyRequestModel(BaseModel):
    profile_id: UUID
    api_key_type_id: UUID
    api_key: str

#class APIKeyTypeModel(BaseModel):
#    id: UUID
#    name: str
#    created_at: datetime
#    description: str

class APIKeyUpdateModel(BaseModel):
    api_key: str

class APIKeyType(BaseModel):
    id: UUID
    created_at: datetime
    name: str | None = None
    description: str | None = None