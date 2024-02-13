import os
from fastapi import FastAPI
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/run")
def run_autogen():
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
    assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
    user_proxy = UserProxyAgent(
        "user_proxy", code_execution_config={"work_dir": "coding"}
    )
    chat_result = user_proxy.initiate_chat(
        assistant, message="Plot a chart of NVDA and TESLA stock price change YTD."
    )
    return {"chat_result": chat_result}
