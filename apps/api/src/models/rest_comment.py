from uuid import UUID
from pydantic import BaseModel

# TODO: This is placed here since the openapi schema of this model cant be generated if its in the src/rest/models directory for some reason
# will move this later on but this works for now 
class PublishCommentRequest(BaseModel):
    lead_id: UUID
    comment: str
    reddit_username: str
    reddit_password: str
