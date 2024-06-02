import arxiv
import os
import diskcache as dc
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader

# Get the current date and format it as YYYY-MM-DD
current_date = datetime.now().strftime("%Y-%m-%d")

# Create a directory to save the results, named based on the current date
output_dir = f"arxiv_results_{current_date}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize the cache
cache = dc.Cache("cache")

# Construct the default API client.
client = arxiv.Client()

# Search for the 100 most recent articles matching the keywords.
search = arxiv.Search(
    query="language model ai artificial intelligence machine learning agents cat:cs",
    max_results=100,
    sort_by=arxiv.SortCriterion.SubmittedDate,
)

results = client.results(search)

for r in results:
    # Define a unique key for caching based on the article's ID
    cache_key = r.entry_id

    # Check if the article is already cached
    if cache_key in cache:
        print(f"Article '{r.title}' already processed. Skipping.")
        continue

    # Define the file name using the title of the paper (sanitize the title to make it a valid file name)
    file_name = r.title.replace(" ", "_").replace("/", "_") + ".txt"
    file_path = os.path.join(output_dir, file_name)

    # Write the title, authors, publication date, and PDF link to the file
    with open(file_path, "w") as file:
        file.write(f"Title: {r.title}\n")
        file.write(f"Published: {r.published}\n")
        file.write(f"Link: {r.pdf_url}\n")
        file.write(f"Abstract: {r.summary}\n\n")

    # Add the article to the cache
    cache.add(cache_key, True)

print(f"Results have been saved to the '{output_dir}' directory")

# Close the cache
cache.close()
