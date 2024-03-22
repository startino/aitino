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

    template = """
    Please write summary of the following text to reduce its length by following these guidelines:
    - Extract information from each sentence and include it in the summary.
    - You use bulleted lists for output, not numbered lists.
    - DO NOT remove any crucial information.
    - IF PRESENT, you must include information about the author such as his profession(or student) and if he knows how to code.
    - DO NOT make up any information that was not present in the original text.

    Text:
    {selftext}
    """

    prompt = PromptTemplate(
        input_variables=["selftext"],
        template=template
    )

    summary_prompt = prompt.format(selftext=selftext)

    summary = llm.invoke(summary_prompt)
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


if __name__ == "__main__":
    # Example of using the summarize_submission function
    summarize_submission(Submission(id="010", url="https://aiti.no", created_utc=00000, title="I need a simple front end to fetch my headless CMS data. Maybe nocode? ", 
                                    selftext="""
                                    Need to build LittleCode/NoCode supply chain NFC Tag website. Low cost. headless cms

Hi. Via storyblok.com (or another headless cms or something? i was also thinking about using wordpress but idk) information about a product (text + images/videos) will be stored.

I need to put the content somehow into a very simple website. The link of the website will be stored into a NFC tag.

there are thousands of ways to do that. What’s the best/easiest way? Actually a wordpress website would be the best way i guess. but i dont really like wordpress that much, it is really slow…

any other CMS you can recommend? or with a head

do you know a cheaper alternative to storybloks? and a way to publish the content easy into a website?

actually i’m a react dev but i didnt code for 2 years now and i need to get this done

maybe i use a react boilerplate website where i fetch the headless CMS content?

or maybe there is a SaaS for my “problem”?

video i would host on bunnycdn (cheapest option) or for free on yt
                                    """))