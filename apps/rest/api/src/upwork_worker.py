import time
from gptrim import trim
from praw.models import Submission
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import AIMessage
from .prompts.upwork_proposals import generate_proposal_prompt


def generate_proposal(post: str) -> str:
    """
    Generate a proposal for a job listing on Upwork
    """

    cost = 0

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    template = """

    {generate_proposal_prompt}


    # Job Listing
    {post}
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["generate_proposal_prompt", "post"],
    )

    chain = prompt | llm

    result = chain.invoke(
        {"generate_proposal_prompt": generate_proposal_prompt, "post": post}
    )

    return str(result.content)
