import logging
import os
from typing import Annotated

import autogen
from autogen.agentchat.contrib.retrieve_assistant_agent import (
    RetrieveAssistantAgent,
)
from autogen.agentchat.contrib.retrieve_user_proxy_agent import (
    RetrieveUserProxyAgent,
)
from fastapi import APIRouter

router = APIRouter(
    prefix="/leon",
    tags=["leon"],
)

logger = logging.getLogger("root")


@router.get("/")
def read_sub():
    return {"message": "Hello World from sub API"}


@router.get("/rag")
def run_rag_crew():
    config_list = autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={
            "model": ["gpt-3.5-turbo"],
        },
    )
    config = {
        "seed": 41,
        "temperature": 0,
        "config_list": config_list,
        "timeout": 60,
    }
    # assistant = RetrieveAssistantAgent(
    #    name="assistant",
    #    system_message="you are an assistant who retrieves context",
    #    llm_config=config
    # )
    #
    # user_proxy = RetrieveUserProxyAgent(
    #    name="rag proxy agent",
    #     retrieve_config={
    #        "task": "qa",
    #        "docs_path": "https://raw.githubusercontent.com/microsoft/autogen/main/README.md",
    #    }
    # )
    #
    # user_proxy.initiate_chat(assistant, message=user_proxy.message_generator, problem="Tell me about autogen")

    termination_msg = lambda x: x.get("content", "").rstrip().endswith("TERMINATE")

    boss = autogen.UserProxyAgent(
        name="Boss",
        is_termination_msg=termination_msg,
        human_input_mode="TERMINATE",
        system_message="The boss who ask questions and give tasks.",
    )

    boss_aid = RetrieveUserProxyAgent(
        name="Boss_Assistant",
        is_termination_msg=termination_msg,
        system_message="Assistant who has extra content retrieval power for solving difficult problems.",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=3,
        retrieve_config={
            "task": "qa",
            "docs_path": [
                "https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Examples/Integrate%20-%20Spark.md",
                "https://raw.githubusercontent.com/microsoft/FLAML/main/website/docs/Research.md",
                os.path.join(os.path.abspath(""), "..", "website", "docs"),
            ],
            "get_or_create": True,
        },
        code_execution_config=False,  # we don't want to execute code in this case.
    )
    coder = autogen.AssistantAgent(
        name="Senior_Python_Engineer",
        is_termination_msg=termination_msg,
        system_message="You are a senior python engineer. Reply `TERMINATE` in the end when everything is done.",
        llm_config={"config_list": config_list, "timeout": 60, "temperature": 0},
    )

    pm = autogen.AssistantAgent(
        name="Product_Manager",
        is_termination_msg=termination_msg,
        system_message="You are a product manager. Reply `TERMINATE` in the end when everything is done.",
        llm_config={"config_list": config_list, "timeout": 60, "temperature": 0},
    )

    reviewer = autogen.AssistantAgent(
        name="Code_Reviewer",
        is_termination_msg=termination_msg,
        system_message="You are a code reviewer. Reply `TERMINATE` in the end when everything is done.",
        llm_config={"config_list": config_list, "timeout": 60, "temperature": 0},
    )

    def retrieve_content(
        message: Annotated[
            str,
            "Refined message which keeps the original meaning and can be used to retrieve content for code generation and question answering.",
        ],
        n_results: Annotated[int, "number of results"] = 3,
    ) -> str:
        # Check if we need to update the context.
        update_context_case1, update_context_case2 = boss_aid._check_update_context(
            message
        )
        if (update_context_case1 or update_context_case2) and boss_aid.update_context:
            boss_aid.problem = message if not hasattr(boss_aid, "problem") else boss_aid.problem  # type: ignore
            _, ret_msg = boss_aid._generate_retrieve_user_reply(message)  # type: ignore
        else:
            _context = {"problem": message, "n_results": n_results}
            ret_msg = boss_aid.message_generator(boss_aid, None, _context)
        return ret_msg if ret_msg else message  # type: ignore

    for caller in [pm, coder, reviewer]:
        d_retrieve_content = caller.register_for_llm(
            description="retrieve content for code generation and question answering.",
            api_style="function",
        )(retrieve_content)

    for executor in [boss, pm]:
        executor.register_for_execution()(d_retrieve_content)

    groupchat = autogen.GroupChat(
        agents=[boss, pm, coder, reviewer],
        messages=[],
        max_round=12,
        speaker_selection_method="round_robin",
        allow_repeat_speaker=False,
    )

    llm_config = {"config_list": config_list, "timeout": 60, "temperature": 0}
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    # Start chatting with the boss as this is the user proxy agent.
    boss.initiate_chat(
        manager,
        message="How to use spark for parallel training in FLAML? Give me sample code.",
    )
