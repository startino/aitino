from gptrim import trim
import os

# Get the directory of the current script file
script_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(script_dir, "startino_business_plan.md"), "r", encoding='utf-8') as file:
    company_context = file.read()

with open(os.path.join(script_dir, "good_examples.md"), "r", encoding='utf-8') as file:
    good_examples = file.read()

with open(os.path.join(script_dir, "bad_examples.md"), "r", encoding='utf-8') as file:
    bad_examples = file.read()

purpose = """
Find potential clients and leads.
"""

context = """
{company_context}
"""

ideal_customer_profile = """
- A non-technical person with a software/app idea that requires software development.
- He has to be non-technical, meaning he shouldn't know how to code or have any
previous experience working in software development.
- He should be looking for a technical co-founder or a software development agency
to help him build his idea.
"""

guidance = """
Relevant Posts might be...:
- Seeking technical co-founders for startups.
- Looking for technical personnel to join startup team.
- In search of software development agencies or technical consultancy services.
- an idea for a software business/startup.

Irrelevant Posts might be...:
- Authored by a technical individual, such as tech founder, software developer, or other job in the software field.
- Showing off existing products or projects.
- Focused on physical/in-person business ventures.
- From businesses already established.
- From individuals seeking employment.
- Regarding projects or products that have already begun development.
- People or agencies offering their own development/coding services.
- Seeking ONLY design services.
- Seeking ONLY to make a simple website (and not an app/project). 
- Related to HOW to do something using a website builder or no code platform (Airtable,Bubble,Webflow,etc)
"""

examples = f"""
Here is a list of good examples and bad examples.

FORMAT:
```
X. [title]
[content]
```

GOOD EXAMPLES:
{good_examples if good_examples else "NONE"}
BAD EXAMPLES:
{bad_examples if bad_examples else "NONE"}
"""

roleplay = """
Imagine you are a super talented virtual assistant.
You have the duty of going through social media posts and determining if they are
relevant to look into for your boss.
"""

calculate_relevance_prompt = trim(f"""
                                  # INSTRUCTIONS
                                  {roleplay}
                                  # PURPOSE
                                  {purpose}
                                  # Ideal Customer Profile
                                  {ideal_customer_profile}
                                  # GUIDANCE  
                                  {guidance}
                                  # CONTEXT
                                  {context}
                                  # EXAMPLES
                                  {examples}

                                                                
""")

