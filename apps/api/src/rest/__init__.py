from typing import List
from saving import save_submission
import diskcache as dc
import mail
from models import FilterQuestion, Lead
import reddit_utils
from llms import evaluate_relevance, invoke_chain, create_chain, summarize_submission, filter_with_questions
from logging_utils import log_relevance_calculation
from interfaces import db
import comment_bot
from praw.models import Submission

# Relevant subreddits to Startino
SUBREDDIT_NAMES="SaaS+SaaSy+startups+YoungEntrepreneurs+NoCodeSaas+nocode+cofounder+Entrepreneur"

def start_reddit_stream():
    # Set up the cache directory
    cache = dc.Cache('./cache')

    subreddits = reddit_utils.get_subreddits(SUBREDDIT_NAMES)

    for submission in subreddits.stream.submissions():

        # Skip if not a submission (for typing)
        if not isinstance(submission, Submission):
            continue

        # TODO: filter by kewords

        # Avoid repeating posts using caching
        is_cached = cache.get(submission.id)
        if (is_cached):
            continue

        # Use LLMs to see if submission is relevant (expensive part)
        evaluated_submission = evaluate_relevance(submission, filter=True)
        
        # If submission is relevant
        if (evaluated_submission.is_relevant):

            # Send email
            mail.send_submission_via_email(evaluated_submission)

            # Save to database
            db.post_lead(Lead(
                redditor=submission.author.name,
                source="THEIRPOST",
                last_event="comment_posted",
                status="subscriber",
                title=submission.title,
                body=submission.selftext,
                url= submission.url))
            
            # Comment on the post
            comment_bot.send_comment(submission)

        # Save to local file and cache
        save_submission(evaluated_submission)
        cache.set(submission.id, submission.id)


if __name__ == "__main__":
    start_reddit_stream()