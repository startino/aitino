# Aitino
[Aitino Web](https://aiti.no) - Our cloud-hosted version of Aitino


## Roadmap
🔥 Feb 16 - Waitlist Launch

⏳ Feb 22 - v0.1.0 Release - Simple functionality for creating and running a team of AI Agents.

⏳ Mar 26 - v0.2.0 Release - Enhanced functionalities (auto-build, applet builder, community features, multi-modal task solving) and making Aitino stand out.

⏳ Apr 17 - v1.0.0 Release - First official release. Final touches will be added to make this truly a remarkable platform.


## What is Aitino

Aitino is an open-source platform that allows for the creation of teams of AI Agents to help users automate high-level tasks and solve complex problems without the need for lengthy and complicated setups.
We're hoping that Aitino can go from prompt to solution in a matter of minutes while only needing seconds from the user to provide the required information like API keys, context, and specific information for the agents to solve the tasks.
Aitino takes the visual form of a node editor as we believe this is one of the easiest to implement and most scalable solutions for both us and the user. It's intuitive and can allow for highly complex teams while also remaining simple for small use cases.

Aitino is built on top of the [Autogen Framework](https://github.com/microsoft/autogen). We also hope to merge some principles applied to other multi-agent system projects like ChatDev and CrewAI as there are some features from those that are out of reach with Autogen alone.


## Aitino Web

**Aitino Web is the cloud-hosted version of Aitino. It uses a subscription model to run Aitino in the cloud. You can start a free trial (coming soon) to see how powerful Aitino really is in a matter of minutes.**
- The source code can be found [here](https://github.com/Futino/futino/tree/alpha/apps/aitino).
- It uses [SvelteKit](https://kit.svelte.dev/) as the framework, [TailwindCSS](https://tailwindcss.com/) for styling, [shacn-svelte](https://www.shadcn-svelte.com/) for components, [Supabase](https://supabase.com/) for database, [Stripe](https://stripe.com/en-hk) for payment processing, and [Vercel](https://vercel.com) for hosting.


## Installation

1. Run `cp .env.example .env` and fill in the necessary environment variables.
2. Install python dependencies, I recommend using a virtual environment.
3. Run `uvicon aitino:app --reload` to start the server.
4. Navigate to `localhost:8000/docs` 

## Contribute
This project welcomes contributions and suggestions. If you are new to GitHub, here is a detailed help source on getting involved with development on GitHub.

If you're passionate about what we're doing at Aitino and would like to get paid while developing, feel free to reach out. We're constantly looking for innovators and passionate developers.
