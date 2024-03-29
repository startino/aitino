import praw
import os
from dotenv import load_dotenv
import reddit_utils
from urllib.parse import quote_plus


load_dotenv()
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

def get_subreddits(subreddit_names:str):
    reddit = praw.Reddit(
        client_id="N8d22rDKxw06lEVozaiDKA",
        client_secret=REDDIT_CLIENT_ID,
        password=REDDIT_PASSWORD,
        user_agent="testscript by u/antopia_hk",
        username="antopia_hk"
    )
    print("Reddit sign in success! Username: ", reddit.user.me())

    subreddits = reddit.subreddit(subreddit_names)
    
    return subreddits


def reply(submission, reply_text):
    reply_template = "[Let me google that for you](https://lmgtfy.com/?q={})"
    url_title = quote_plus(submission.title)
    reply_text = reply_template.format(url_title)
    submission.reply(reply_text)

def compose():
    print('sdf')

if __name__ == "__main__":
    subreddits = get_subreddits("futino")
    
    