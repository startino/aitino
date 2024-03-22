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

GUIDELINES:
Relevant Posts might be...:
- Seeking technical co-founders for startups.
- Looking for technical personnel to join startup team.
- In search of software development agencies or technical consultancy services.
- an idea for a software business/startup.

Irrelevant Posts might be...:
- Showing off existing products or projects.
- Focused on physical/in-person business ventures.
- Authored by technical individuals, such as tech founders, software developers, or other job in the software field.
- From businesses already established.
- From individuals seeking employment.
- Regarding projects or products that have already begun development.
- People or agencies offering their own development/coding services.
- Seeking ONLY design services.
- Seeking ONLY to make a simple website (and not an app/project). 
- Related to HOW to do something using a website builder or no code platform (Airtable,Bubble,Webflow,etc)

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

calculate_relevance_prompt = trim(f"""
Imagine you are a super talented virtual assistant.
You have the duty of going through social media posts and determining if they are
relevant to look into.

{user_context}

""")