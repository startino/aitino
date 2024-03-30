from models import EvaluatedSubmission
import csv
import pandas as pd

posts_filepath = "./reddit_posts.csv"

def save_submission(submission: EvaluatedSubmission):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(posts_filepath, sep=",")

    # Append the new row to the DataFrame
    new_row = {'id': submission.id, 'timestamp': submission.created_utc, 'url': submission.url, 'title': submission.title, 'body': submission.selftext, 'is_relevant': submission.is_relevant, 'cost' : submission.cost, 'reason': submission.reason}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)


    # Write the DataFrame back to the CSV file
    df.to_csv(posts_filepath, index=False)
