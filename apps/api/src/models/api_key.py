from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel

class APIKeyRequestModel(BaseModel):
    profile_id: UUID
    api_key_type_id: UUID
    api_key: str

class APIKeyResponseModel(BaseModel):
    id: UUID
    created_at: datetime
    profile_id: UUID
    api_key_type_id: UUID
    api_key: str