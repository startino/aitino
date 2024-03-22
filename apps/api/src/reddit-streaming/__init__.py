from typing import List
from saving import save_submission
import diskcache as dc
import mail
from models import Submission
import reddit_utils
from llms import invoke_chain, create_chain, summarize_submission
from logging_utils import log_relevance_calculation

# Relevant subreddits to Startino
SUBREDDIT_NAMES="SaaS+SaaSy+startups+sveltejs+webdev+YoungEntrepreneurs+NoCodeSaas+nocode+EntrepreneuerRideAlong+cofounder+Entrepreneur+smallbusiness+advancedentrepreneur+business"

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
        is_relevant, cost, reason = evaluate_relevance(submission)

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
        print(f"Result: {result}")
        reasons.append(result['reason'])

    mean_llm_certainty = total_llm_certainty / iterations
    mean_vote_certainty = calculate_certainty(votes)

    print(votes)
    
    # Calculate final certainty
    certainty = mean_llm_certainty * llm_weight + mean_vote_certainty * vote_weight

    # TODO: Make model of this
    return majority_vote(votes), certainty, cost, reasons


def evaluate_relevance(submission: Submission) -> tuple[bool, float, str]:
    """
    Determines the relevance of a submission using GPT-3.5-turbo, 
    optionally escalating to GPT-4-turbo for higher accuracy.

    Parameters:
    - submission: The submission object to be evaluated.

    Returns:
    - is_relevant (bool): Final relevance decision based on the used model(s).
    - total_cost (float): The total cost incurred from relevance calculations.
    """

    ## TODO: switch from certainty method to funnel method
    # I realized certainty method doesn't work with GPT-3. might work with multiple GOOD models. 
    # but at that point its more expensive. so scratch that.
    # totally_irrelevant = relevant_at_all(submission)z
    total_cost = 0
    is_relevant, certainty, gpt4_cost, reasons = calculate_relevance('gpt-4-turbo-preview', 1, submission)
    log_relevance_calculation('gpt-4-turbo-preview', submission, is_relevant, gpt4_cost, reasons)

    total_cost += gpt4_cost

    # I've come to conclude that GPT-3.5 sucks.
    # So I am temporarily removing the extra steps
    # TODO: Give this another go but with better prompting
    # and use "relevance_score" as a float instead "is_relevant" as a bool
    # Since it seems like if it is picking between yes/no,
    # its inputted certainty will always be high
    if (False):
        is_relevant, certainty, gpt4_cost = calculate_relevance('gpt-4-turbo-preview', 3, submission)

        print(f"GPT-4 Relevant: {is_relevant}")
        print(f"GPT-4 Certainty: {certainty}")
        print(f"GPT-4 Cost: {gpt4_cost} ")
        
        total_cost += gpt4_cost

        print(f"Total Cost: {total_cost} \n")

        # Return the results from GPT-4-turbo
        return is_relevant, total_cost
    else:
        print(f"Total Cost: {total_cost}")
        print("\n")
        # Return the results from GPT-3.5-turbo since its accurate and valid
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