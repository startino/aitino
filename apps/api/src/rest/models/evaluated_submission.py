from praw.models import Submission

class EvaluatedSubmission(Submission):
    def __init__(self, submission: Submission, is_relevant: bool, cost: float, reason: str, qualifying_question: str | None = None, source: str | None = None):
        super().__init__(**submission.__dict__)
        self.is_relevant = is_relevant
        self.cost = cost
        self.reason = reason
        self.qualifying_question = qualifying_question
        self.source = source
