import autogen
import logging
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from src.autobuilder import build_agents
from src.dependencies import rate_limit_profile
from src.lib.auth import get_current_user
from src.lib.improver import improve_prompt
from src.models import Profile, ImproveInsertRequest

router = APIRouter()


@router.get("/")
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@router.post("/improve")
def improve(
    request: ImproveInsertRequest,
) -> str:
    try:
        return improve_prompt(
            request.prompt,
            request.word_limit,
            request.prompt_type,
            request.profile_id,
            request.temperature,
        )
    except Exception as e:
        logging.error(f"got error when improving prompt: {e}")
        raise e


@router.get(
    "/auto-build",
    dependencies=[Depends(rate_limit_profile(limit=3, period_seconds=60))],
)
def auto_build_crew(general_task: str) -> str:
    agents = build_agents.BuildAgents()
    auto_build_agent = agents.create_all_in_one_agent()
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        system_message="test admin",
        code_execution_config=False,
        human_input_mode="NEVER",
        default_auto_reply="Reply TERMINATE if the task has been solved at full satisfaction. If you instead require more information reply TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.",
        max_consecutive_auto_reply=1,
    )
    chat_result = user_proxy.initiate_chat(
        auto_build_agent, message=general_task, silent=True
    )
    crew_frame = chat_result.chat_history[-1]["content"]
    return crew_frame


@router.get("/me")
def get_profile_from_header(current_user=Depends(get_current_user)) -> Profile:
    return current_user
