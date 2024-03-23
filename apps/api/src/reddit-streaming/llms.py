import time
from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models import Submission, RelevanceResult
from gptrim import trim
from dotenv import load_dotenv
import os
from langchain_community.callbacks import get_openai_callback
from prompting import calculate_relevance_prompt, context as company_context, purpose
from boolean_parser import BooleanOutputParser
from langchain.output_parsers import PydanticOutputParser
from models import FilterOutput
from dummy_submissions import relevant_submissions, irrelevant_submissions

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
    
    llm = ChatOpenAI(model=model, temperature=0.1, openai_api_key=OPENAI_API_KEY, verbose=True)

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
                result = chain.invoke({"query": f"{calculate_relevance_prompt} \n\n POST CONTENT:\n ```{submission.title}\n\n {submission.selftext}```"})
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
    It aims to reduce the token count of the submission content by 50%.

    Parameters:
    - submission (Submission): The submission object to be summarized.

    Returns:
    - The submission object with the selftext replaced with a shorter version (the summary).
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

    # Trim the submission content for cost savings
    selftext = trim(submission.selftext)

    # Short submissions are not summarized
    if (llm.get_num_tokens(selftext) < 150):
        return submission

    template = f"""
    # Welcome Summary Writer!
    Your job is to help a Virtual Assistant in filtering Reddit posts.
    You'll help by summarizing the content of a Reddit post to remove any useless parts.

    # Guidelines
    - Extract information from each sentence and include it in the summary.
    - Use bullet points to list the main points.
    - DO NOT remove any crucial information.
    - IF PRESENT, you must include information about the author such as his profession(or student) and if he knows how to code.
    - DO NOT make up any information that was not present in the original text.
    - Commendations and encouragements should be removed.
    # Body Text To Summarize
    ```
    {selftext}
    ```


    # Here is more information for context

    {company_context}

    ## Purpose of this process
    {purpose}

    """


    summary = llm.invoke(template)
    summarized_selftext = summary.content

    # Calculate token reduction
    pre_token_count = llm.get_num_tokens(selftext)
    post_token_count = llm.get_num_tokens(summarized_selftext)
    reduction = ( pre_token_count - post_token_count ) / pre_token_count * 100

    # Print the token reduction
    print(f"Token reduction : {reduction:.3f}%")

    # Update the submission object with the summarized content
    submission.selftext = summarized_selftext

    return submission


# uses gpt-3.5-turbo to filter out irrelevant posts by using simple yes no questions
def filter_submission_with_questions(submission: Submission, questions: List[str]) -> tuple[bool, str]:
    """
    Filters out irrelevant posts by asking simple yes/no questions to the LLM.
    The questions are generated using GPT-3.5-turbo.

    If any one of the questions is answered with a NO, the submission is considered irrelevant.

    Parameters:
    - submission (Submission): The submission object to be filtered.
    - questions (List[str]): A list of yes-no questions to be asked to the LLM. 
    YES answers mean the submission is kept (kept).
    NO answers mean the submission is discarded (irrelevant).

    Returns:
    - A boolean indicating whether the submission is relevant.
    (True = relevant, False = irrelevant)
    - The question that caused the submission to be filtered out.
    """
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)

    template = """
    You are a helpful assistant that needs to filter out irrelevant posts.
    You will read a Reddit post, and then answer a yes-no question based on the 
    post's content and provide the source. 
    If the specific information is not present in the post, then answer True.

    {format_instructions}
    
    # Question
    {question}

    # Post
    Title: {title}
    Content: {selftext}
    """

    parser = PydanticOutputParser(pydantic_object=FilterOutput)

    for question in questions:
        prompt = PromptTemplate(
            template=template,
            input_variables=["question", "title", "selftext"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        chain = prompt | llm | parser
        filter_output = chain.invoke({"question": question, "title": submission.title, "selftext": submission.selftext})
        print(f"Question: {question}")
        print(f"Result: {filter_output}")
        filter_output = FilterOutput.parse_obj(filter_output)
        if not filter_output.answer:
            return False, filter_output.source
    
    return True, "SUCCESS"

if __name__ == "__main__":
    # Test the filter_submission_with_questions function
    submission = relevant_submissions[1]
    questions = ["Is the author not a tech related person? i.e. a coder, programmer, software developer.",
                "Is the post NOT asking for employment or looking for a job?",
                "The project has not already started development, correct?",
                "Is the post NOT about someone offering their own development or coding services?",
    ]
    # print(filter_submission_with_questions(submission, questions))

    submission = relevant_submissions[0]
    print(summarize_submission(submission).selftext)