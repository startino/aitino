import pandas as pd
import os

from models import EvaluatedSubmission

# Get the current file's directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Get the sibling file's path
posts_filepath = os.path.join(current_dir, "./reddit_posts.csv")


def save_submission(submission: EvaluatedSubmission):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(posts_filepath, sep=",")

    # Append the new row to the DataFrame
    new_row = {
        "id": submission.submission.id,
        "timestamp": submission.submission.created_utc,
        "url": submission.submission.url,
        "title": submission.submission.title,
        "body": submission.submission.selftext,
        "is_relevant": submission.is_relevant,
        "cost": submission.cost,
        "reason": submission.reason,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Write the DataFrame back to the CSV file
    df.to_csv(posts_filepath, index=False)
