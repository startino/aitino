#import autogen

from langchain.tools.file_management.read import ReadFileTool
#from src.tooling.tools import CircumferenceTool, get_file_path_of_example

#def generate_llm_config(tool):
#    function_schema = {
#        "name": tool.name.lower().replace(" ", "_"),
#        "description": tool.description,
#        "parameters": {
#            "type": "object",
#            "properties": {},
#            "required": [],
#        },
#    }
#
#    if tool.args is not None:
#        function_schema["parameters"]["properties"] = tool.args
#    
#    return function_schema

def generate_llm_config(tools) -> list[dict]:
    schemas = []
    for tool in tools:
        function_schema = {
            "name": tool.name.lower().replace(" ", "_"),
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }

        if tool.args is not None:
            function_schema["parameters"]["properties"] = tool.args
        schemas.append(tool)
    
    return schemas
read_file_tool = ReadFileTool()

def thing_that_compares_agent_tool_list_with_tools(tool_names: list[str]) -> list[dict]: # pseudo code
    ...
#custom_tool = CircumferenceTool(description="Use this tool when you need to calculate a circumference using the radius of a circle")
# 
#base_config_list = autogen.config_list_from_json(
#    "OAI_CONFIG_LIST",
#    filter_dict={
#        "model": ["gpt-3.5-turbo"],
#    },
#)
# 
#llm_config = {
#    "functions": [
#        generate_llm_config(custom_tool),
#        generate_llm_config(read_file_tool),
#    ],
#    "config_list": base_config_list,
#    "timeout": 120,
#}
# 
#user_proxy = autogen.UserProxyAgent(
#    name="user_proxy",
#    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
#    human_input_mode="NEVER",
#    max_consecutive_auto_reply=4,
#    code_execution_config={
#        "work_dir": "coding",
#        "use_docker": False,
#    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
#)
# 
#user_proxy.register_function(
#    function_map={
#        custom_tool.name: custom_tool._run,
#        read_file_tool.name: read_file_tool._run,
#    }
#)
# 
#chatbot = autogen.AssistantAgent(
#    name="chatbot",
#    system_message="For coding tasks, only use the functions you have been provided with. Reply TERMINATE when the task is done.",
#    llm_config=llm_config,
#)
# 
#user_proxy.initiate_chat(
#    chatbot,
#    message=f"Read the file with the path {get_file_path_of_example()}, then calculate the circumference of a circle that has a radius of that files contents.",  # 7.81mm in the file
#    llm_config=llm_config,
#)