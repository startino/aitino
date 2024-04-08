from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel

class APIKeyRequestModel(BaseModel):
    profile_id: UUID
    api_key_type_id: UUID
    api_key: str

class APIKeyTypeModel(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    description: str

class APIKeyResponseModel(BaseModel):
    id: UUID
    created_at: datetime
    profile_id: UUID
    api_key_type: APIKeyTypeModel | None = None
    api_key: str

class APIKeyUpdateModel(BaseModel):
    api_key: str