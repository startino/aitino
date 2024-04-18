from uuid import UUID

from pydantic import BaseModel


class FalseLead(BaseModel):
    lead_id: UUID
    submission_id: UUID
    correct_reason: str
