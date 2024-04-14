from praw import Reddit
from praw.models import Subreddits
from dotenv import load_dotenv
import os

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")


def get_reddit_instance(username, password):
    return Reddit(
        client_id="xCs8EA8-_cIY6ZsPod5EIw",
        client_secret=REDDIT_CLIENT_ID,
        password=password,
        user_agent="testscript by u/antopia_hk",
        username=username,
    )


def get_subreddits(subreddit_names: str, username: str, password: str):
    reddit = get_reddit_instance(username, password)

    print("Reddit sign in success! Username: ", reddit.user.me())

    subreddits: Subreddits = reddit.subreddit(subreddit_names)

    return subreddits
