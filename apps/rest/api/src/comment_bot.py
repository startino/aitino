import logging
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .models import EvaluatedSubmission, RedditComment, PublishCommentResponse
from .dummy_submissions import relevant_submissions, irrelevant_submissions
from .prompts import generate_comment_prompt
from .interfaces import db
from .reddit_utils import get_reddit_instance

from dotenv import load_dotenv
import os

# Load Enviornment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def generate_comment(title: str, selftext: str, instructions: str = "") -> str:
    llm = AzureChatOpenAI(
        azure_deployment="gpt-4-turbo",
        temperature=0.3,
    )

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=RedditComment)

    template = (
        generate_comment_prompt
        + """

    {format_instructions}
    
    # Post
    Title: {title}
    Content: {selftext}

    # Additional instructions
    {instructions}
    """
    )

    prompt = PromptTemplate(
        template=template,
        input_variables=["title", "selftext", "instructions"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    # Generate a comment
    result = chain.invoke(
        {
            "title": title,
            "selftext": selftext,
            "instructions": instructions,
        }
    )

    return RedditComment(**result).comment


def publish_comment(
    id, text: str, username: str, password: str
) -> PublishCommentResponse | None:
    lead = db.get_lead(id)
    print(lead)
    if lead is None or lead.status == "subscriber":
        logging.error(f"Lead with id {id} not found")
        return None

    submission_id = lead.reddit_id
    reddit = get_reddit_instance(username, password)
    submission = reddit.submission(submission_id)
    submission.reply(text)
    # If a comment was published, it means the submission is relevant.
    # So update the human answer to TRUE. Just a shortcut to avoid double work.
    db.update_human_review_for_submission(id, human_answer=True)

    return db.update_lead(lead.id, status="subscriber", last_event="comment_posted")
