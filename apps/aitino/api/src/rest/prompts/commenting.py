import os

from gptrim import trim

# Get the directory of the current script file
script_dir = os.path.dirname(os.path.realpath(__file__))

with open(
    os.path.join(script_dir, "startino_business_plan.md"), "r", encoding="utf-8"
) as file:
    company_context = file.read()

with open(
    os.path.join(script_dir, "good_comment_examples.md"), "r", encoding="utf-8"
) as file:
    good_examples = file.read()

with open(os.path.join(script_dir, "bad_examples.md"), "r", encoding="utf-8") as file:
    bad_examples = file.read()

purpose = """
Introduce myself and Futino and quickly capture interest with a relevant value proposition, setting the stage for further engagement and relationship building.
"""

context = f"""
{company_context}
"""

guidance = """
- Keep the comment concise and to the point.
- Don't mention about cost effectiveness of Futino.
- Mention how we gaurantee our dedication through our services for equity model.
"""

examples = f"""
Here is a list of good examples and bad examples that 
you can use to guide your response.

FORMAT:
```
1. [example 1]

2. [example 2]

n. ...

```

GOOD EXAMPLES:
{good_examples if good_examples else "NONE"}
BAD EXAMPLES:
{bad_examples if bad_examples else "NONE"}
"""

roleplay = """
Imagine you are a super talented virtual assistant.
You have the duty of going through Reddit posts and 
writing comments that fulfill the purpose.
"""

generate_comment_prompt = trim(
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
