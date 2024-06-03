import arxiv
from arxiv import Result
import os
import diskcache as dc
from datetime import datetime, timedelta
from langchain_community.document_loaders import PyPDFLoader

# Get the current date and format it as YYYY-MM-DD
current_date = datetime.now().strftime("%Y-%m-%d")

# Initialize the cache
cache = dc.Cache("cache")


def get_papers(query: str) -> list[Result]:
    # Construct the default API client.
    client = arxiv.Client()

    # Search for the 100 most recent articles matching the keywords.
    search = arxiv.Search(
        query,
        max_results=1000,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    results = client.results(search)

    papers = []

    # Calculate the date 7 days ago
    seven_days_ago = datetime.now() - timedelta(days=7)

    # Add the papers to the cache
    for r in results:
        # Define a unique key for caching based on the article's ID
        cache_key = r.entry_id

        # Check if the article is already cached
        if cache_key in cache:
            print(f"Article '{r.title}' already processed. Skipping.")
            continue

        # Check if the article was posted within the last 7 days
        article_date = r.published.replace(tzinfo=None)
        if article_date < seven_days_ago:
            print(f"Article '{r.title}' is older than 7 days. Skipping.")
            continue

        # Add the article to the cache
        cache.add(cache_key, True)

        papers.append(r)

    # Close the cache
    cache.close()

    print(len(papers))

    return papers


get_papers("language model ai artificial intelligence machine learning agents cat:cs")
