from gptrim import trim
import os

# Get the directory of the current script file
script_dir = os.path.dirname(os.path.realpath(__file__))

with open(
    os.path.join(script_dir, "startino_business_plan.md"), "r", encoding="utf-8"
) as file:
    company_context = file.read()

with open(
    os.path.join(script_dir, "good_proposal_examples.md"), "r", encoding="utf-8"
) as file:
    good_examples = file.read()

with open(
    os.path.join(script_dir, "bad_proposal_examples.md"), "r", encoding="utf-8"
) as file:
    bad_examples = file.read()

purpose = """
Write a proposal for a job listing in order to close the client.
"""

context = f"""
{company_context}
"""

guidance = """
## Output the proposal in the following format
```
PROPOSAL
Dear Startup Team, I am ....
```

## Job listing format
```
[Title]
Posted [x] days ago
[Location]

[Description]
```
When writing, remember that you are writing on behalf of Futino.

**Effective Strategies for Crafting Winning Upwork Proposals**

**Introduction to Upwork Proposals**
Upwork, a leading global freelancing platform, offers numerous opportunities for freelancers to connect with clients and secure freelance work. A crucial element in this process is the Upwork proposal—comparable to a cover letter—that serves as your first interaction with a potential client. This proposal allows you to highlight your suitability for the project, demonstrate your understanding of the client’s needs, and outline how you plan to address their specific requirements.

**The Role of Upwork Proposals**
Proposals on Upwork are more than just introductory messages; they are strategic tools designed to capture the client’s attention and differentiate you from the competition. Given the sheer volume of job postings and applicants on Upwork, your proposal must be succinct yet compelling, ensuring it conveys your understanding of the project and your ability to deliver results efficiently.

**Crafting a Standout Upwork Proposal**
1. **Start Strong:** Begin with a personalized greeting that leverages any client-specific insights you can glean from their Upwork profile or feedback. Addressing the client by name, for instance, can make your proposal more engaging and personal.
2. **Demonstrate Understanding:** Quickly affirm your grasp of the client’s main challenges and goals. This shows you’ve thoroughly read the project description and are prepared to address their needs.
3. **Present Your Strategy:** Clearly outline your approach to the project. Describe the steps you will take, the methodology you intend to employ, and the timeline you anticipate. This part should reassure the client of your structured and thoughtful process in tackling their project.
4. **Highlight Relevant Experience:** Include brief examples or links to similar work you’ve done in the past. This is crucial for building credibility and trust, showing the client that you have successfully handled similar challenges.
5. **Conclude with a Strong Closing:** Summarize why you are the ideal candidate for the project, touching on your understanding of the project, your relevant experience, and your readiness to begin immediately. Make sure this summary is tailored to the specifics of the job posting.

**Additional Tips for Enhancing Your Proposal**
- **Conciseness is Key:** Keep your proposal concise and to the point. Avoid lengthy descriptions; instead, focus on brevity and relevance to the client’s needs.
- **Add Personal Touches:** Where appropriate, include a personal touch or a unique element, such as a video introduction linked in your proposal, to make your submission stand out.
- **Continuous Improvement:** Always seek feedback and refine your approach. Experiment with different styles and structures to discover what resonates best with clients on Upwork.

"""

examples = f"""
Here is a list of good examples and bad examples that 
you can use to guide your response.

GOOD EXAMPLES:
{good_examples if good_examples else "NONE"}
BAD EXAMPLES:
{bad_examples if bad_examples else "NONE"}
"""

roleplay = """
Imagine you are an experienced virtual assistant who is helping the company find
clients on upwork by writing compelling proposals for the job listings.
"""

generate_proposal_prompt = trim(
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
