import autogen
import os

from pathlib import Path

class BuildAgents():
    def create_task_simplifier(self):
        config_list = autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": ["gpt-4-turbo-preview"],
            },
        )
        config = {
            "seed": 41,
            "temperature": 0.0,
            "config_list": config_list,
            "timeout": 120,
        }
        return autogen.ConversableAgent(
            name="""tasksimplifier-testagent""",
            system_message=f"""Task simplifier. Your job is to take a given task and turn it into multiple smaller tasks, all working to solve the larger task. 
            Split these tasks up in a way where agents who are specialized in a certain field will get the task most suited for them. For example, 
            if the main task would include a subtask to write software in python, it would be benficial to write this task in a way where an agent with the role Software Engineer
            with skills in Python could handle it. Output these tasks as a list of strings, putting every task inside square brackets and seperating each task with a comma. 
            For example: a list with the objects banana, apple and orange would be written as "[banana, apple, orange]" """,
            llm_config=config,
        )

    def create_employer(self):
        config_list = autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": ["gpt-4-turbo-preview"],
            },
        )
        config = {
            "seed": 41,
            "temperature": 0.0,
            "config_list": config_list,
            "timeout": 120,
        }
        return autogen.ConversableAgent(
            name="""agentemployer-testagent""",
            system_message=f"""Agent employer. You will recieve a list of different subtasks that are created to solve a main task. 
            Your job is to analyze these and give each subtask an agent who will solve this task. 
            These agents will have a name, job title, a prompt for how they do their job and a prompt for how to solve the task they have been given. 
            Format the prompts in markdown. """,
            llm_config=config,
        )

    def create_all_in_one_agent(self):
        config_list = autogen.config_list_from_json(
            "OAI_CONFIG_LIST",
            filter_dict={
                "model": ["gpt-4-turbo-preview"],
            },
        )

        config = {
            "seed": 41,
            "temperature": 0.0,
            "config_list": config_list,
            "timeout": 120,
        }

        with open(
            Path(os.getcwd(), "src", "prompts", "autobuild", "team-specialist.md"),
            "r",
            encoding="utf-8",
        ) as f:
            system_prompt = f.read()
            return autogen.AssistantAgent(
                name="""teamspecialist""",
                system_message=system_prompt,
                # should add something to parse a list of good agents from the database, give them to this agent and give those agents as examples for it to use during team creation
                # should also add something that is better at dynamically making teams of agents that work together (my solution here is to tell it to make teams, which is not optimal)
                llm_config=config,
            )