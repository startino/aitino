import logging
from autogen import ConversableAgent
import autogen
from fastapi import APIRouter

router = APIRouter(
    prefix="/daniel",
    tags=["daniel"],
)

logger = logging.getLogger("root")


@router.get("/")
def read_sub():
    return {"message": "Hello World from sub API"}


@router.get("/test")
def read_test():
    return {"message": "Hello  from sub API"}


# @router.get("/run-crew")
# def run_crew():
#     base_model: str = "gpt-3.5-turbo"
#     base_config_list = autogen.config_list_from_json(
#         "OAI_CONFIG_LIST",
#         filter_dict={
#             "model": [base_model],
#         },
#     )
#     base_config = {
#         "temperature": 0,
#         "config_list": base_config_list,
#         "timeout": 120,
#     }
#     lovelyfriend = ConversableAgent(
#         "my lovely friend",
#         system_message="You like giving out apple math questions",
#         human_input_mode="NEVER",
#         llm_config=base_config,
#     )
#     joe = ConversableAgent(
#         "joe",
#         system_message="Your name is Joe and you hate math questions, but you answer apple math questions",
#         human_input_mode="NEVER",  # Never ask for human input.
#         llm_config=base_config,
#     )
#     result = lovelyfriend.initiate_chat(joe, max_turns=2)
#     print(result)
