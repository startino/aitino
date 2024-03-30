from praw import Reddit
from praw.models import Subreddits
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

def get_subreddits(subreddit_names:str):
    reddit = Reddit(
        client_id="N8d22rDKxw06lEVozaiDKA",
        client_secret=REDDIT_CLIENT_ID,
        password=REDDIT_PASSWORD,
        user_agent="testscript by u/antopia_hk",
        username="antopia_hk"
    )
    print("Reddit sign in success! Username: ", reddit.user.me())

    subreddits: Subreddits = reddit.subreddit(subreddit_names)
    
    return subreddits

