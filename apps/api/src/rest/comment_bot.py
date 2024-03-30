from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models import EvaluatedSubmission, RedditComment
from dummy_submissions import relevant_submissions, irrelevant_submissions
from prompts import generate_comment_prompt

from dotenv import load_dotenv
import os

# Load Enviornment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_comment(submission: EvaluatedSubmission) -> RedditComment:
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.3)

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=RedditComment)

    template = generate_comment_prompt + """

    {format_instructions}
    
    # Post
    Title: {title}
    Content: {selftext}
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["title", "selftext"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    # Generate a comment
    result = chain.invoke({"title": submission.title, "selftext": submission.selftext})

    return RedditComment(**result)


def send_comment(submission):
    text = generate_comment(submission)
    submission.reply(text)


if __name__ == "__main__":
    submission = relevant_submissions[0]
    print(generate_comment(submission))