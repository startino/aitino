'input': '"composition": {
    "agents": [
        {
            "role": "Reddit Scraper",
            "system_message": "Scrape Reddit stories based on specified criteria such as subreddit, keywords, or time frame. Extract the necessary metadata including the story title, author, and full text."
        },
        {
            "role": "Content Summarizer",
            "system_message": "Use OpenAI to generate concise summaries of the scraped Reddit stories. Ensure the summaries capture the essence of the stories while being brief."
        },
        {
            "role": "Excel Integrator",
            "system_message": "Input the original Reddit stories along with their summaries and metadata into an Excel sheet. Organize the data in a structured manner for easy reading and analysis."
        },
        {
            "role": "Quality Assurance Agent",
            "system_message": "Review the summaries and Excel sheet entries for accuracy and coherence. Ensure that the summaries accurately reflect the content of the stories and that the Excel sheet is free of errors and well-organized."
        }
    ]
}'