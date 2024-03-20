import csv
import pandas as pd

posts_filepath = "./reddit_posts.csv"

def save_submission_notpandas(submission, is_relevant):
    timestamp, url, title, body, is_relevant = submission.created_utc, submission.url, submission.title, submission.selftext, is_relevant
    with open(posts_filepath, 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, url, title, body, is_relevant])


def save_submission(submission, is_relevant, cost):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(posts_filepath, sep=",")

    # Append the new row to the DataFrame
    new_row = {'id': submission.id, 'timestamp': submission.created_utc, 'url': submission.url, 'title': submission.title, 'body': submission.selftext, 'is_relevant': is_relevant, 'cost' : cost}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)


    # Write the DataFrame back to the CSV file
    df.to_csv(posts_filepath, index=False)
