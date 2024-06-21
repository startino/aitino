from gptrim import trim
import os

# Get the directory of the current script file
script_dir = os.path.dirname(os.path.realpath(__file__))

with open(
    os.path.join(script_dir, "startino_business_plan.md"), "r", encoding="utf-8"
) as file:
    company_context = file.read()

with open(os.path.join(script_dir, "good_examples.md"), "r", encoding="utf-8") as file:
    good_examples = file.read()

with open(os.path.join(script_dir, "bad_examples.md"), "r", encoding="utf-8") as file:
    bad_examples = file.read()

purpose = """
Your purpose is to filter research articles that are not useful for your boss.
"""

context = """
{company_context}
"""

guidance = """
Topics of interest might be...:
- Language models (LLMs)
- Language processing (NLP)
- AI Agents

Papers that are not relevant might be...:
- Purely theoretical with no practical applications
- Highly mathematical with no practical applications
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
You have the duty of going through computer science research articles and determining if they are
relevant to look into for your boss.
"""

evaluate_relevance = trim(
    f"""
        # INSTRUCTIONS
        {roleplay}
        # PURPOSE
        {purpose}
        # GUIDANCE  
        {guidance}
        # CONTEXT
        {context}
        # EXAMPLES
        {examples}
"""
)
