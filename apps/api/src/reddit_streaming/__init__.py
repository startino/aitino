from typing import List
from saving import save_submission
import diskcache as dc
import mail
from models import Submission, FilterQuestion, Lead
import reddit_utils
from llms import evaluate_relevance, invoke_chain, create_chain, summarize_submission, filter_with_questions
from logging_utils import log_relevance_calculation
from interfaces import db

# Relevant subreddits to Startino
SUBREDDIT_NAMES="SaaS+SaaSy+startups+YoungEntrepreneurs+NoCodeSaas+nocode+cofounder+Entrepreneur"

def start_reddit_stream():
    # Set up the cache directory
    cache = dc.Cache('./cache')

    subreddits = reddit_utils.get_subreddits(SUBREDDIT_NAMES)

    submission: Submission
    for submission in subreddits.stream.submissions():
        # TODO: filter by kewords

        submission = Submission(
            id=submission.id,
            author=submission.author.name,
            title=submission.title,
            selftext=submission.selftext,
            created_utc=submission.created_utc,
            url=submission.url
        )

        # Avoid repeating posts using caching
        is_cached = cache.get(submission.id)
        if (is_cached):
            continue

        # Use LLMs to see if submission is relevant (expensive part)
        is_relevant, cost, reason = evaluate_relevance(submission, filter=True)
        
         # Send email if its relevant
        if (is_relevant):
            mail.send_submission_via_email(submission)

            # Save to database
            db.post_lead(Lead(
                redditor=submission.author,
                source="Reddit",
                last_event="comment_posted",
                status="subscriber",
                title=submission.title,
                body=submission.selftext,
                url= submission.url))
            # Comment on the post
            # TODO: implement this

        # Save to local file and cache
        save_submission(submission, is_relevant, cost, reason)
        cache.set(submission.id, submission.id)

        


if __name__ == "__main__":
    start_reddit_stream()