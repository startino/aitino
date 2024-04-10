import pandas as pd
import os

import comment_bot
from models import Lead
from interfaces import db
from models import EvaluatedSubmission

# Get the current file's directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Get the sibling file's path
posts_filepath = os.path.join(current_dir, "./reddit_posts.csv")


def update_db_with_submission(evalutated_submission: EvaluatedSubmission):
    db.post_evaluated_submission(evalutated_submission)
    if evalutated_submission.is_relevant:
        # Get the reddit submission from the EvaluatedSubmission
        submission = evalutated_submission.submission
        # Convert the submission to a Lead
        lead = Lead(
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
            comment=comment_bot.generate_comment(evalutated_submission).comment,
        )
        db.post_lead(lead)
