import logging
from uuid import UUID

import autogen
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.routers import api_provider

from . import mock as mocks
from .auth import get_current_user
from .autobuilder import build_agents
from .crew import AutogenCrew
from .dependencies import (
    RateLimitResponse,
    rate_limit,
    rate_limit_profile,
    rate_limit_tiered,
)
from .improver import PromptType, improve_prompt
from .interfaces import db
from .models import Profile
from .routers import agents, api_provider, api_keys
from .routers import auth as auth_router
from .routers import (
    billing_information,
    crews,
    messages,
    profiles,
    rest,
    sessions,
    subscriptions,
    tiers,
    tools,
)
from .routers.sandbox import (
    daniel,
    leon,
)

logger = logging.getLogger("root")
logger.setLevel("INFO")

app = FastAPI()

app.include_router(sessions.router)
app.include_router(messages.router)
app.include_router(crews.router)
app.include_router(agents.router)
app.include_router(profiles.router)
app.include_router(api_keys.router)
app.include_router(auth_router.router)
app.include_router(api_provider.router)
app.include_router(tools.router)
app.include_router(subscriptions.router)
app.include_router(rest.router)
app.include_router(tiers.router)
app.include_router(billing_information.router)

daniel.include_router(daniel.router)
app.mount("/daniel", daniel)

leon.include_router(leon.router)
app.mount("/leon", leon)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:8080",
        "http://localhost:8081",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
        "https://aiti.no",
        "https://api.aiti.no",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get(
    "/improve", dependencies=[Depends(rate_limit_profile(limit=4, period_seconds=60))]
)
def improve(
    word_limit: int, prompt: str, prompt_type: PromptType, temperature: float
) -> str:
    return improve_prompt(word_limit, prompt, prompt_type, temperature)


@app.get(
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


@app.get("/me")
def get_profile_from_header(current_user=Depends(get_current_user)) -> Profile:
    return current_user
