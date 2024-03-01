import autogen

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
            system_message="""Task simplifier. Your job is to take a main task and turn it into multiple smaller tasks, all working to solve this main task. 
            Split these tasks up in a way where agents who are specialized in a certain field will get the task most suited for them. For example, 
            if the main task would include a subtask to write software in python, it would be benficial to write this task in a way where an agent with the role Software Engineer
            with skills in Python could handle it. Output these tasks as a list of strings, for example: a list of a banana, an apple and an orange would be written as "[banana, apple, orange]"
            Reply TERMINATE if the task has been solved at full satisfaction. If you instead require more information reply TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
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
            system_message="""Agent employer. You will recieve a list of different subtasks that are created to solve a main task. 
            Your job is to analyze these and give each subtask an agent who will solve this task. 
            These agents will have a name, job title, a prompt for how they do their job and a prompt for how to solve the task they have been given. 
            Format the prompts in markdown. 
            Reply TERMINATE if the task has been solved at full satisfaction. If you instead require more information reply TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.""",
            llm_config=config,
        )