from typing import List
from saving import save_submission
import diskcache as dc
import mail
from models import FilterQuestion, Lead
import reddit_utils
from relevance_bot import (
    evaluate_relevance,
    invoke_chain,
    create_chain,
    summarize_submission,
    filter_with_questions,
)
from logging_utils import log_relevance_calculation
from interfaces import db
import comment_bot
from praw.models import Submission

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Relevant subreddits to Startino
SUBREDDIT_NAMES = (
    "SaaS+SaaSy+startups+YoungEntrepreneurs+NoCodeSaas+nocode+cofounder+Entrepreneur"
)

logger = logging.getLogger("root")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:8080",
        "http://localhost:8081",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
        "https://aiti.no",
        "https://api.aiti.no",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Will be run on server 24/7
def start_reddit_stream():
    # Set up the cache directory
    cache = dc.Cache("./cache")

    subreddits = reddit_utils.get_subreddits(SUBREDDIT_NAMES)

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
                    comment=comment_bot.generate_comment(
                        evaluated_submission).comment,
                )
            )

        # Save to local file and cache
        save_submission(evaluated_submission)
        cache.set(submission.id, submission.id)


@app.get(
    "/publish-comment",
)
def publish_comment(submission_id, comment):
    comment_bot.publish_comment(submission_id, comment)


if __name__ == "__main__":
    start_reddit_stream()
