import time
from typing import List
import os
from arxiv import Result
from dotenv import load_dotenv

from gptrim import trim
from praw.models import Submission
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_community.callbacks import get_openai_callback
from langchain_community.document_loaders import PyPDFLoader

from models import RelevanceResult
from prompts import evaluate_relevance
from utils import majority_vote, calculate_certainty_from_bools
from logging_utils import log_relevance_calculation


# Load Enviornment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def filter_papers(papers: list[Result]) -> list[Result]:
    """
    Filter the papers based on the relevance.
    """
    filtered_papers = []

    llm = AzureChatOpenAI(azure_deployment="gpt-4-turbo")

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=RelevanceResult)

    cost = 0.0

    for paper in papers:
        loader = PyPDFLoader(paper.pdf_url)
        pages = loader.load_and_split()

        prompt = PromptTemplate(
            template="\n{format_instructions}\n\n {relevance_prompt} \n\n # Paper {paper}",
            input_variables=["relevance_prompt", "paper"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        chain = prompt | llm | parser

        try:
            with get_openai_callback() as cb:
                result = chain.invoke(
                    {"relevance_prompt": evaluate_relevance, "paper": paper.summary}
                )
                cost += cb.total_cost
                evaluated_paper = RelevanceResult(**result)
                if evaluated_paper.is_relevant:
                    filtered_papers.append(paper)

        except Exception as e:
            print(f"An error occurred while invoke_chain: {e}")
            time.sleep(2)  # Wait for 10 seconds before trying again

        print(f"Cost: {cost}")
    return filtered_papers
