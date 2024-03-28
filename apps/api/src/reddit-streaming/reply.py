import reddit_utils
from llms import invoke_chain, create_chain, summarize_submission
from logging_utils import log_relevance_calculation
from urllib.parse import quote_plus

reply_template = "[Let me google that for you](https://lmgtfy.com/?q={})"


# Relevant subreddits to Startino
SUBREDDIT_NAMES="futino"

subreddits = reddit_utils.get_subreddits(SUBREDDIT_NAMES)

for submission in subreddits.stream.submissions():
    
    url_title = quote_plus(submission.title)
    reply_text = reply_template.format(url_title)

    submission.reply(reply_text)