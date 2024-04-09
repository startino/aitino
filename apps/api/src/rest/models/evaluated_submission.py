from typing import Optional
from praw.models import Submission
from pydantic import BaseModel, ConfigDict


# TODO: inhertit Submission class to just extend it with additional fields
# I struggled with this since its not a pydantic class and I could not find a
# way to inherit it without dictionary bugs
class EvaluatedSubmission(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    submission: Submission
    is_relevant: bool
    cost: float
    reason: Optional[str] = None
    qualifying_question: Optional[str] = None
