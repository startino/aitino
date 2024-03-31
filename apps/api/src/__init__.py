import logging
from typing import Any
from uuid import UUID

import autogen
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from . import mock as mocks
from .autobuilder import build_agents
from .crew import Crew
from .dependencies import (
    RateLimitResponse,
    rate_limit,
    rate_limit_profile,
    rate_limit_tiered,
)
from .improver import PromptType, improve_prompt
from .interfaces import db
from .models import CrewModel, Message, Session
from .parser import parse_input_v0_2 as parse_input
from .routers import agents, crews, messages, sessions

logger = logging.getLogger("root")

app = FastAPI()

sessions.router.include_router(messages.router)
app.include_router(sessions.router)
app.include_router(crews.router)
app.include_router(agents.router)

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


@app.get("/compile", dependencies=[Depends(rate_limit(3, 30, "compile"))])
def compile(id: UUID) -> dict[str, str | CrewModel]:
    message, composition = db.get_compiled(id)

    return {
        "prompt": message if message else "Not Found",
        "composition": composition if composition else "Not Found",
    }


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
