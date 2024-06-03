from praw import Reddit
from praw.models import Subreddits, Submission
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
import diskcache as dc
import logging

from pathlib import Path

from .relevance_bot import evaluate_relevance
from .saving import update_db_with_submission
from .reddit_utils import get_subreddits, get_reddit_instance

load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")


current_directory = Path(__file__).resolve().parent

# Path to the sibling file
cache_filepath = current_directory / "cache"

# Set up the cache directory
cache = dc.Cache(cache_filepath)


class RedditStreamWorker:
    def __init__(self, subreddit_names: str, username: str, password: str):
        self._running = False
        self.subreddits = get_subreddits(subreddit_names, username, password)

    def start(self):
        self._running = True
        while self._running:
            try:
                if not REDDIT_USERNAME or not REDDIT_PASSWORD:
                    raise TypeError("couldnt find username or password in env vars")

                for submission in self.subreddits.stream.submissions(pause_after=-1):
                    if submission is None:
                        break
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

                    # Save to db and cache
                    update_db_with_submission(evaluated_submission)
                    cache.set(submission.id, submission.id)
            except Exception as e:
                logging.error(f"Error when evalauting submission. Error: {e} \n Submission: {submission}")
                cache.set(submission.id, submission.id)

    def stop(self):
        self._running = False
