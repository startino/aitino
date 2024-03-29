from typing import List
from saving import save_submission
import diskcache as dc
import mail
from models import Submission, FilterQuestion
import reddit_utils
from llms import invoke_chain, create_chain, summarize_submission, filter_with_questions
from logging_utils import log_relevance_calculation

# Relevant subreddits to Startino
SUBREDDIT_NAMES="SaaS+SaaSy+startups+YoungEntrepreneurs+NoCodeSaas+nocode+cofounder+Entrepreneur"

def start_reddit_stream():
    # Set up the cache directory
    cache = dc.Cache('./cache')

    subreddits = reddit_utils.get_subreddits(SUBREDDIT_NAMES)

    submission: Submission
    for submission in subreddits.stream.submissions():
        # TODO: filter by kewords

        # Avoid repeating posts using caching
        is_cached = cache.get(submission.id)
        if (is_cached):
            continue

        # Use LLMs to see if submission is relevant (expensive part)
        is_relevant, cost, reason = evaluate_relevance(submission, filter_with_questions=True)

        # Send email if its relevant
        if (is_relevant):
            mail.send_submission_via_email(submission)
        
        # Save to csv file and cache
        save_submission(submission, is_relevant, cost, reason)
        cache.set(submission.id, submission.id)


def calculate_relevance(model: str,iterations: int, submission: Submission):
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
    votes: List[bool] = []
    
    total_llm_certainty = 0
    total_vote_certainty = 0

    mean_llm_certainty = 0
    mean_vote_certainty= 0

    # Setup the weights
    vote_weight = 0
    llm_weight = 1 - vote_weight

    # If more than one iteration, then uses last index
    reasons: List[str] = []

    # Calculate mean relevance scores using 3.5-turbo
    for _ in range(0,iterations):
        submission = summarize_submission(submission)
        chain = create_chain(model)
        result, run_cost = invoke_chain(chain, submission)

        votes.append(result['is_relevant'])
        cost += run_cost

        total_llm_certainty += result['certainty']

        reasons.append(result['reason'])

    mean_llm_certainty = total_llm_certainty / iterations
    mean_vote_certainty = calculate_certainty(votes)
    
    # Calculate final certainty
    certainty = mean_llm_certainty * llm_weight + mean_vote_certainty * vote_weight

    # TODO: Make model of this
    return majority_vote(votes), certainty, cost, reasons


def evaluate_relevance(submission: Submission, filter: bool) -> tuple[bool, float, str]:
    """
    Determines the relevance of a submission using GPT-3.5-turbo, 
    optionally escalating to GPT-4-turbo for higher accuracy.

    Parameters:
    - submission: The submission object to be evaluated.

    Returns:
    - is_relevant (bool): Final relevance decision based on the used model(s).
    - total_cost (float): The total cost incurred from relevance calculations.
    """

    if (filter):
        questions = [
            FilterQuestion(question="Is the author himself a tech related person? i.e. a coder, programmer, software developer.", reject_on=True),
            FilterQuestion(question="Has the project already started development?", reject_on=True),
            FilterQuestion(question="Is the author currently engaged in job searching activities and promoting their technical expertise?", reject_on=True),
            FilterQuestion(question="Is the author starting a non-tech business? Like a bakery, garden business, salon, etc.", reject_on=True),
        ]
        
        keep_submission, source = filter_with_questions(submission, questions)
        if not keep_submission:
            return False, 0, source
    
    is_relevant, certainty, gpt4_cost, reasons = calculate_relevance('gpt-4-turbo-preview', 1, submission)
    log_relevance_calculation('gpt-4-turbo-preview', submission, is_relevant, gpt4_cost, reasons[0])

    # I've come to conclude that GPT-3.5 sucks.
    # So I am temporarily removing the method of using certainty
    # TODO: Give this another go but with better prompting
    # and use "relevance_score" as a float instead "is_relevant" as a bool
    # Since it seems like if it is picking between yes/no,
    # its certainty will always be high

    return is_relevant, total_cost, reasons[-1]


def majority_vote(bool_list: List[bool]) -> bool:
    return sum(bool_list) > len(bool_list) / 2


def calculate_certainty(bool_list: List[bool]) -> float:
    length = len(bool_list)
    total = sum(bool_list)
    
    true_certainty = total / length
    false_certainty = (length-total) / length

    return max(true_certainty, false_certainty)


if __name__ == "__main__":
    start_reddit_stream()