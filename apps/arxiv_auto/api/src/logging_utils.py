from praw.models import Submission
from datetime import datetime


def log_relevance_calculation(
    model: str, submission: Submission, is_relevant: bool, cost: float, reason: str
):
    """
    Logs the calculation of the relevance of a submission.
    """
    # TODO: use a logging package
    print(f"Model: {model}")
    print(f"URL: {submission.url}")
    print(f"Datetime: {datetime.fromtimestamp(submission.created_utc)}")
    print(f"Title: {submission.title}")
    print(f"Content: {submission.selftext[:150]}")
    print(f"Cost: {cost}")
    print(f"Is Relevant: {'Yes' if is_relevant else 'No'}")
    print(f"Reason: {reason}")
    print("\n\n")

