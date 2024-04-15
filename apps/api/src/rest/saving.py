import os

from . import comment_bot
from .models import Lead
from .interfaces import db
from .models import EvaluatedSubmission, SavedSubmission

# Get the current file's directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Get the sibling file's path
posts_filepath = os.path.join(current_dir, "./reddit_posts.csv")


def update_db_with_submission(evalutated_submission: EvaluatedSubmission):
    # Convert the EvaluatedSubmission to a SavedSubmission
    # TODO: I don't know if using a separate model for this is necessary
    # or if we can just save the EvaluatedSubmission directly and extract the
    # title and body from the submission property.
    saved_submission = SavedSubmission(
        reddit_id=evalutated_submission.submission.id,
        title=evalutated_submission.submission.title,
        body=evalutated_submission.submission.selftext,
        url=evalutated_submission.submission.url,
        is_relevant=evalutated_submission.is_relevant,
        reason=evalutated_submission.reason,
        cost=evalutated_submission.cost,
        qualifying_question=evalutated_submission.qualifying_question,
    )
    db.post_evaluated_submission(saved_submission)
    if evalutated_submission.is_relevant:
        # Get the reddit submission from the EvaluatedSubmission
        submission = evalutated_submission.submission
        # Convert the submission to a Lead
        lead = Lead(
            submission_id=saved_submission.id,
            prospect_username=submission.author.name,
            source="their_post",
            last_event="discovered",
            status="under_review",
            data={
                "title": submission.title,
                "body": submission.selftext,
                "url": submission.url,
            },
            reddit_id=submission.id,
            comment=comment_bot.generate_comment(
                title=evalutated_submission.submission.title,
                selftext=evalutated_submission.submission.selftext,
            ),
        )
        db.post_lead(lead)
