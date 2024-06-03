import time
from typing import List
import os
from dotenv import load_dotenv

from gptrim import trim
from praw.models import Submission
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_community.callbacks import get_openai_callback

from .models import EvaluatedSubmission, RelevanceResult, FilterOutput, FilterQuestion
from .prompts import calculate_relevance_prompt, context as company_context, purpose
from .dummy_submissions import relevant_submissions, irrelevant_submissions
from .utils import majority_vote, calculate_certainty_from_bools
from .logging_utils import log_relevance_calculation


# Load Enviornment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def create_chain(model: str):
    """
    Creates a processing chain for evaluating the relevance of a submission using a specified language model.

    Parameters:
    - model (str): The name of the deployed azure model to be used for generating responses.

    Returns:
    - A processing chain configured to use the specified azure language model and to parse its output.
    """

    llm = AzureChatOpenAI(
        azure_deployment=model,
        temperature=0.1,
    )

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
                result = chain.invoke(
                    {
                        "query": f"{calculate_relevance_prompt} \n\n #POST CONTENT:\n ```{submission.title}\n{submission.selftext}```"
                    }
                )
                # TODO: Do some cost analysis and saving (for long term insights)
                return result, cb.total_cost
        except Exception as e:
            print(f"An error occurred while invoke_chain: {e}")
            time.sleep(2)  # Wait for 10 seconds before trying again

    raise RuntimeError(
        "Failed to invoke chain after 3 attempts. Most likely no more credits left or usage limit has been reached."
    )


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
    llm = AzureChatOpenAI(
        azure_deployment="gpt-4-turbo",
        temperature=0,
    )

    # Trim the submission content for cost savings
    selftext = trim(submission.selftext)

    # Short submissions are not summarized
    if llm.get_num_tokens(selftext) < 150:
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
    post_token_count = llm.get_num_tokens(str(summarized_selftext))
    reduction = (pre_token_count - post_token_count) / pre_token_count * 100

    # Print the token reduction
    print(f"Token reduction : {reduction:.3f}%")

    # Update the submission object with the summarized content
    submission.selftext = summarized_selftext

    return submission


# uses gpt-3.5-turbo to filter out irrelevant posts by using simple yes no questions
def filter_with_questions(
    submission: Submission, questions: list[FilterQuestion]
) -> tuple[bool, str, float]:
    """
    Filters out irrelevant posts by asking simple yes/no questions to the LLM.
    The questions are generated using GPT-3.5-turbo.

    If any one of the questions is answered with a NO, the submission is considered irrelevant.

    Parameters:
    - submission (Submission): The submission object to be filtered.
    - questions (list[str]): A list of yes-no questions to be asked to the LLM.
    YES answers mean the submission is kept (kept).
    NO answers mean the submission is discarded (irrelevant).

    Returns:
    - A boolean indicating whether the submission is relevant.
    (True = relevant, False = irrelevant)
    - The question that caused the submission to be filtered out.
    """

    cost = 0

    llm = AzureChatOpenAI(
        azure_deployment="gpt-4-turbo",
        temperature=0,
    )
    parser = PydanticOutputParser(pydantic_object=FilterOutput)

    template = """
    You are a helpful assistant that helps to filter posts.
    You will read a Reddit post, and then answer a yes-no question based on the 
    post's content and provide the source.

    The term "OP" refers to Original Poster, the person who made the post, also
    known as the author.

    {format_instructions}
    
    # Question
    {question}

    # Post
    Title: {title}
    Content: {selftext}
    """

    for question in questions:

        prompt = PromptTemplate(
            template=template,
            input_variables=["question", "title", "selftext"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | llm | parser

        # Error checking since gpt-3.5 sucks at json formatting lol
        for i in range(10):
            try:
                with get_openai_callback() as cb:
                    result = chain.invoke(
                        {
                            "question": question.question,
                            "title": submission.title,
                            "selftext": submission.selftext,
                        }
                    )
                    # TODO: Do some cost analysis and saving (for long term insights)
                    cost += cb.total_cost
                break
            except Exception as e:
                print(f"An error occurred while filtering using questions: {e}")
                time.sleep(2)  # Wait for 10 seconds before trying again
                if i == 10:
                    return True, "ERRORED", cost

        filter_output = FilterOutput.parse_obj(result)

        if question.reject_on == filter_output.answer:
            # Remove the submission
            return False, filter_output.source, cost

    return True, "SUCCESS", cost


def calculate_relevance(
    model: str, iterations: int, submission: Submission
) -> EvaluatedSubmission:
    """
    Calculates the relevance of a submission by iterating multiple times
    and also calculates the mean certainty of the repetitions.

    Parameters:
    - model (str): The model name to use for relevance determination.
    - iterations (int): The number of times to run the calculation.
    - submission: The submission object to be evaluated.

    Returns:
    - majority_vote (bool): Whether the majority of iterations deemed the submission relevant.
    - mean_certainty (float): The average certainty across all iterations.
    - cost (int): The total cost incurred during the calculations.
    """

    cost = 0
    votes: list[bool] = []

    total_llm_certainty = 0
    total_vote_certainty = 0

    mean_llm_certainty = 0
    mean_vote_certainty = 0

    # Setup the weights
    vote_weight = 0
    llm_weight = 1 - vote_weight

    # If more than one iteration, then uses last index
    reasons: list[str] = []

    # Calculate mean relevance scores using 3.5-turbo
    for _ in range(0, iterations):

        # TODO: implement when summarization becomes more accurate
        # submission = summarize_submission(submission)

        chain = create_chain(model)
        result, run_cost = invoke_chain(chain, submission)

        votes.append(result["is_relevant"])
        cost += run_cost

        total_llm_certainty += result["certainty"]

        reasons.append(result["reason"])

    mean_llm_certainty = total_llm_certainty / iterations
    mean_vote_certainty = calculate_certainty_from_bools(votes)

    # Calculate final certainty
    certainty = mean_llm_certainty * llm_weight + mean_vote_certainty * vote_weight

    evaluated_submission = EvaluatedSubmission(
        submission=submission, is_relevant=votes[0], cost=float(cost), reason=reasons[0]
    )

    return evaluated_submission


def evaluate_relevance(submission: Submission, filter: bool) -> EvaluatedSubmission:
    """
    Determines the relevance of a submission using GPT-3.5-turbo,
    optionally escalating to GPT-4-turbo for higher accuracy.

    Parameters:
    - submission: The submission object to be evaluated.

    Returns:
    - is_relevant (bool): Final relevance decision based on the used model(s).
    - total_cost (float): The total cost incurred from relevance calculations.
    """

    if filter:
        questions = [
            FilterQuestion(
                question="Is the author himself an IT person? is/was he a programmer? is/was he a software developer?",
                reject_on=True,
            ),
            FilterQuestion(
                question="Is the author currently engaged in job searching activities and promoting their technical expertise?",
                reject_on=True,
            ),
            FilterQuestion(
                question="Is the author starting a non digital business? Like a bakery, garden business, salon, etc.",
                reject_on=True,
            ),
        ]

        keep_submission, source, cost = filter_with_questions(submission, questions)
        if not keep_submission:
            print("Filtered out submission")
            print("Source: ", source)
            print("Title: ", submission.title)
            print("Selftext: ", submission.selftext)
            print("\n")
            return EvaluatedSubmission(
                submission=submission, is_relevant=False, cost=cost, reason=source
            )

    evalualuated_submission = calculate_relevance("gpt-4o", 1, submission)
    log_relevance_calculation(
        "gpt-4o",
        submission,
        evalualuated_submission.is_relevant,
        evalualuated_submission.cost,
        evalualuated_submission.reason,
    )

    # I've come to conclude that GPT-3.5 sucks.
    # So I am temporarily removing the method of using certainty
    # TODO: Give certainty another go but with better prompting
    # and use "relevance_score" as a float instead "is_relevant" as a bool
    # Since it seems like if it is picking between yes/no,
    # its certainty will always be high

    return evalualuated_submission


if __name__ == "__main__":
    # Test the filter_submission_with_questions function
    submission = relevant_submissions[4]
    questions = [
        FilterQuestion(
            question="Is the author himself a tech related person? i.e. a coder, programmer, software developer.",
            reject_on=True,
        ),
        FilterQuestion(
            question="Has the project already started development?", reject_on=True
        ),
        FilterQuestion(
            question="Is the author currently engaged in job searching activities and promoting their technical expertise?",
            reject_on=True,
        ),
        FilterQuestion(
            question="Is the author starting a non-tech business? Like a bakery, garden business, salon, etc.",
            reject_on=True,
        ),
    ]
    print(filter_with_questions(submission, questions))

    submission = relevant_submissions[0]
    # print(summarize_submission(submission).selftext)
