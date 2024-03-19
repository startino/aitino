from pyexpat import model
from tabnanny import verbose
from click import prompt
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor
from boolean_parser import BooleanOutputParser
from langchain_community.callbacks import get_openai_callback
from save_utils import save_submission
from dotenv import load_dotenv
import os
import praw
from datetime import datetime
import time 
import diskcache as dc

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")


INSTRUCTIONS_PROMPT = """
You are a VA that will go through emails that contain social media posts (from Reddit, Linkedin, or Twitter) and determine if they are relevant for me, your boss, to look into.
You will be provided the url to the post, the posts contents, and the requirements of what I'm looking for in a post. You will then determine if the post is relevant or not.

If the post is relevant type "RELEVANT". If the post is irrelevant, type "IRRELEVANT". 
"""

RELEVANT_PROMPT = """
Context:
I am starting a software development agency targeted towards non-tech founders trying to build their software idea.
We are calling what we do "co-founder as a service", as we are providing the tasks that a technical co-founder would do for a startup but as a consultancy.
We would like our VA to filter posts for us to give us the most relevant ones to look at. 
We will be using the most relevant ones as a way to find potential clients.

Guidance:
- Accept posts that are people looking for a technical co-founder or a technical person to join their startup.
- Accept posts that are people looking for a software development agency or a technical consultancy.
"""

# Set up the cache directory
cache = dc.Cache('./cache')

def reddit_stream():
    reddit = praw.Reddit(
        client_id="N8d22rDKxw06lEVozaiDKA",
        client_secret=REDDIT_CLIENT_ID,
        user_agent="reddit_bot",
    )
    subreddit = reddit.subreddit("SaaS+SaaSy+startups+sveltejs+webdev+YoungEntrepreneurs+NoCodeSaas+nocode+EntrepreneuerRideAlong+cofounder+Entrepreneur+smallbusiness+advancedentrepreneur+business")
    for submission in subreddit.stream.submissions():
        # TODO: filter by kewords
        is_cached = cache.get(submission.id)
        if (is_cached):
            continue
        is_relevant = calculate_relevance(submission)
        save_submission(submission, is_relevant)


def calculate_relevance(submission):

    # TODO: create cache and check if submission has already been processed (for cost savings)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                INSTRUCTIONS_PROMPT,
            ),
            (
                "user",
               "{input}"
            ),
           

        ]
    )
    output_parser = BooleanOutputParser(true_val="RELEVANT", false_val="IRRELEVANT")
    chain = prompt | llm | output_parser

    with get_openai_callback() as cb:
        result = chain.invoke({"input": f"{RELEVANT_PROMPT} \n\n POST CONTENT:\n ```{submission.title}\n\n {submission.selftext}```"})

        print(f"Time: {datetime.fromtimestamp(submission.created_utc)}")
        print(f"URL: {submission.url}")
        print(f"Relevant: {result}")
        print(f"Cost: {cb.total_cost} \n")
    
    return result


def main():
    reddit_stream()


if __name__ == "__main__":
    main()