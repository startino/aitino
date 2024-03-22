from distutils.command import clean
import time

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models import Submission, RelevanceResult
from gptrim import trim
from dotenv import load_dotenv
import os
from langchain_community.callbacks import get_openai_callback
from prompting import calculate_relevance_prompt

# Load Enviornment variables

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



def create_chain(model: str):
    """
    Creates a processing chain for evaluating the relevance of a submission using a specified language model.

    The chain is composed of a prompt template, a language model, and a parser to interpret the model's output as a Pydantic object.

    Parameters:
    - model (str): The name of the language model to be used for generating responses.

    Returns:
    - A processing chain configured to use the specified language model and to parse its output.
    """
    
    llm = ChatOpenAI(model=model, temperature=0.2, openai_api_key=OPENAI_API_KEY)

    # Set up a parser + inject instructions into the prompt template.
    parser = JsonOutputParser(pydantic_object=RelevanceResult)

    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | llm | parser
    return chain


def invoke_chain(chain, submission: Submission) -> tuple[RelevanceResult, float]:
    """
    Invokes the processing chain on a submission to evaluate its relevance and calculates the associated cost.

    This function executes the chain with a constructed query from the submission's content, capturing the relevance result and the cost of the operation.

    Parameters:
    - chain: The processing chain to be invoked for the relevance evaluation.
    - submission (Submission): The submission object containing the title and content to be evaluated.

    Returns:
    - A tuple containing the relevance result as a Pydantic object and the total cost of the operation.
    """
    for _ in range(3):
        try:
            with get_openai_callback() as cb:
                result = chain.invoke({"query": f"{calculate_relevance_prompt} \n\n POST CONTENT:\n ```{submission.title}\n\n {trim(submission.selftext)}```"})
                # TODO: Do some cost analysis and saving (for long term insights)
                return result, cb.total_cost
        except Exception as e:
            print(f"An error occurred while invoke_chain: {e}")
            time.sleep(10)  # Wait for 10 seconds before trying again

    raise Exception("Failed to invoke chain after 3 attempts")


def summarize_submission(submission: Submission) -> Submission:
    """
    Summarizes the content of a submission using LLMs.
    Uses a soft summarizing strength and only summarises each paragraph.

    Parameters:
    - submission (Submission): The submission object to be summarized.

    Returns:
    - The submission object with the selftext replaced with a shorter version (the summary).
    """
    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

    # Trim the submission content or cost savings
    selftext = trim(submission.selftext)

    template = """
    Please write summary of the following text to reduce its length in half (roughly):

    {selftext}
    """

    prompt = PromptTemplate(
        input_variables=["selftext"],
        template=template
    )

    summary_prompt = prompt.format(selftext=selftext)
    
    num_tokens = llm.get_num_tokens(summary_prompt)
    print (f"This prompt + essay has {num_tokens} tokens")
    
    summary = llm.invoke(summary_prompt)
    
    print (f"Summary: {summary.content}")
    print ("\n")

    return submission


if __name__ == "__main__":
    # Example of using the summarize_submission function
    summarize_submission(Submission(id="010", url="https://aiti.no", created_utc=00000, title="Hype me up or dissuade me", 
                                    selftext="""
                                    I'm a business analyst with a fully specced out app and have been approaching Devs for the build for a web app/hybrid app mvp.

Initial estimates are around $25000. I'm having more sessions with other Devs to get comparable quotes.

I'm in a position where I could afford to do this but I was initially (potentially naievely) hoping for something around $10000...

Question is.. go forward with this as a 'why not' attempt to start this business or take a step back, more market/customer research/potentially find investment etc...

So.. hype me up or dissuade me 🙃
                                    """))