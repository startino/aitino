import os
from typing import List

from dotenv import load_dotenv
from .saving import save_submission
import diskcache as dc
import mail
from .models import Lead
from .reddit_utils import get_subreddits
from .relevance_bot import evaluate_relevance,
from .interfaces import db
from .comment_bot import generate_comment
from praw.models import Submission

import logging

# Relevant subreddits to Startino
SUBREDDIT_NAMES = (
    "SaaS+SaaSy+startups+YoungEntrepreneurs+NoCodeSaas+nocode+cofounder+Entrepreneur"
)

load_dotenv()
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")

logger = logging.getLogger("root")


# Will be run on server 24/7
def start_reddit_stream():
    # Set up the cache directory
    cache = dc.Cache("./cache")
    if not REDDIT_USERNAME or not REDDIT_PASSWORD:
        raise TypeError("couldnt find username or password in env vars")

    subreddits = get_subreddits(SUBREDDIT_NAMES, REDDIT_USERNAME, REDDIT_PASSWORD)

    for submission in subreddits.stream.submissions():
        # Skip if not a submission (for typing)
        if not isinstance(submission, Submission):
            continue

        # TODO: filter by kewords

        # Avoid repeating posts using caching
        is_cached = cache.get(submission.id)
        if is_cached:
            continue

        # Use LLMs to see if submission is relevant (expensive part)
        evaluated_submission = evaluate_relevance(submission, filter=True)

        # If submission is relevant
        if evaluated_submission.is_relevant:
            # Send email
            # mail.send_submission_via_email(evaluated_submission)
            # Save to database
            db.post_lead(
                Lead(
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
                    comment=generate_comment(evaluated_submission).comment,
                )
            )

        # Save to local file and cache
        save_submission(evaluated_submission)
        cache.set(submission.id, submission.id)


if __name__ == "__main__":
    start_reddit_stream()
