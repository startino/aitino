from urllib.parse import quote_plus

import praw
import os
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")


def reddit_stream():
    reddit = praw.Reddit(
        client_id="N8d22rDKxw06lEVozaiDKA",
        client_secret=REDDIT_CLIENT_ID,
        user_agent="reddit_bot",
    )

    subreddit = reddit.subreddit("Startups")
    for submission in subreddit.stream.submissions():
        process_submission(submission)


def process_submission(submission):
    return (submission.title, submission.selftext)


if __name__ == "__main__":
    main()