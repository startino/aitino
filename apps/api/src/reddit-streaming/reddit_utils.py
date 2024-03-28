import praw
import os
from dotenv import load_dotenv

load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")

def get_subreddits(subreddit_names:str):
    reddit = praw.Reddit(
        client_id="N8d22rDKxw06lEVozaiDKA",
        client_secret=REDDIT_CLIENT_ID,
        password="20051103jorge",
        user_agent="testscript by u/antopia_hk",
        username="antopia_hk"
    )
    print(reddit.user.me())
    subreddits = reddit.subreddit(subreddit_names)
    
    return subreddits