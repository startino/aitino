from pydantic import BaseModel
from uuid import UUID


class FalseLead(BaseModel):
    lead_id: UUID
    submission_id: UUID
    correct_reason: str
