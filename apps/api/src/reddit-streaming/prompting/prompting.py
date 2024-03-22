from gptrim import trim
import os

# Get the directory of the current script file
script_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(script_dir, "startino_business_plan.md"), "r") as file:
    company_context = file.read()

with open(os.path.join(script_dir, "good_examples.md"), "r") as file:
    good_examples = file.read()

with open(os.path.join(script_dir, "bad_examples.md"), "r") as file:
    bad_examples = file.read()

purpose = """
We will be using the relevant posts as a way to find leads.
"""

# The users personal context
user_context = f"""
{purpose}

GUIDANCE:
- Relevant posts will include people looking for a technical co-founder or a technical person to join their startup.
- Relevant posts might people include looking for a software development agency or a technical consultancy.
- Irrelevant posts might include people already with a product built or coded out.
- Most posts relating to physical/in-person businesses are irrelevant.
- If the author of the post is a technical person, tech founder, or knows how to code, it is likely irrelevant.
- If they have started their business a while ago, it is likely irrelevant.
- If they are looking for a job, it is likely irrelevant.
- If they have already started building their project, it is likely irrelevant.
- Irrelevant posts will include people offering their OWN services from their development agency or consultancy.

ABOUT THE COMPANY:
{company_context}
"""

examples = """
Here is a list of good examples and bad examples for you to use in your job.

GOOD EXAMPLES:
{good_examples}
BAD EXAMPLES:
{bad_examples}
"""

prompt = f"""
Imagine you are a super talented virtual assistant.
You have the duty of going through social media posts and determining if they are
relevant to look into.

{user_context}

{examples}
"""

prompt = trim(prompt)