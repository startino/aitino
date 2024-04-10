import os
from typing import List

from dotenv import load_dotenv
from saving import update_db_with_submission
import diskcache as dc
import mail
from models import FilterQuestion, Lead
from reddit_utils import get_subreddits
from relevance_bot import (
    evaluate_relevance,
)
from interfaces import db
from comment_bot import generate_comment
from praw.models import Submission

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

# Relevant subreddits to Startino
SUBREDDIT_NAMES = (
    "SaaS+SaaSy+startups+YoungEntrepreneurs+NoCodeSaas+nocode+cofounder+Entrepreneur"
)

load_dotenv()
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")

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

        # Save to local file and cache
        update_db_with_submission(evaluated_submission)
        cache.set(submission.id, submission.id)


if __name__ == "__main__":
    start_reddit_stream()
