import asyncio
import logging
import re
from typing import Any
from uuid import UUID

import autogen
from autogen import Agent, ConversableAgent
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from . import mock as mocks
from .autobuilder import build_agents
from .crew import Crew
from .dependencies import rate_limit, rate_limit_profile, rate_limit_tiered
from .improver import PromptType, improve_prompt
from .interfaces import db
from .models import CrewModel, Message, Session
from .parser import parse_input_v0_2 as parse_input

logger = logging.getLogger("root")

app = FastAPI()

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
    "/improve", dependencies=[Depends(rate_limit_profile(limit=4, period_seconds=30))]
)
def improve(
    word_limit: int, prompt: str, prompt_type: PromptType, temperature: float
) -> str:
    return improve_prompt(word_limit, prompt, prompt_type, temperature)


@app.get("/crew", dependencies=[Depends(rate_limit_tiered)])
async def run_crew(
    id: UUID,
    profile_id: UUID,
    background_tasks: BackgroundTasks,
    session_id: UUID | None = None,
    reply: str | None = None,
    mock: bool = False,
) -> dict:
    if reply and not session_id:
        raise HTTPException(
            status_code=400,
            detail="If a reply is provided, a session_id must also be provided.",
        )
    if session_id and not reply:
        raise HTTPException(
            status_code=400,
            detail="If a session_id is provided, a reply must also be provided.",
        )

    if mock:
        message, composition = parse_input(mocks.v0_2_0_composition)
    else:
        message, composition = db.get_compiled(id)

    if reply:
        message = reply

    if not message or not composition:
        raise HTTPException(status_code=400, detail=f"Failed to get crew with id {id}")

    session = db.get_session(session_id) if session_id else None
    cached_messages = db.get_messages(session_id) if session_id else None

    if session_id and not session:
        raise HTTPException(
            status_code=400,
            detail=f"Session with id {session_id} not found",
        )

    if session_id and not cached_messages:
        raise HTTPException(
            status_code=400,
            detail=f"Session with id {session_id} found, but has no messages",
        )

    if session is None:
        session = Session(
            crew_id=id,
            profile_id=profile_id,
        )
        db.post_session(session)

    async def on_reply(
        recipient: ConversableAgent,
        messages: list[dict] | None = None,
        sender: Agent | None = None,
        config: Any | None = None,
    ) -> None:
        logger.debug(f"on_reply: {recipient.name} {messages}")
        # This function is called when an LLM model replies
        if not messages:
            logger.error("on_reply: No messages")
            return
        if len(messages) == 0:
            logger.error("on_reply: No messages")
            return

        raw_msg = messages[-1]

        if not raw_msg.get("name"):
            logger.warn(f"on_reply: No name\n{raw_msg}")
            raw_msg["name"] = None
        if not raw_msg.get("content"):
            logger.error(f"on_reply: No content\n{raw_msg}")
            return
        if not raw_msg.get("role"):
            logger.error(f"on_reply: No role\n{raw_msg}")
            return

        logger.info(f"on_reply: {recipient.name} {raw_msg}")

        recipient_id = None  # None means admin
        sender_id = None  # None means admin
        for agent in composition.agents:
            if (
                f"""{agent.role.replace(' ', '')}-{agent.title.replace(' ', '')}"""
                == recipient.name
            ):
                recipient_id = agent.id
            if (
                f"""{agent.role.replace(' ', '')}-{agent.title.replace(' ', '')}"""
                == raw_msg["name"]
            ):
                sender_id = agent.id

        if recipient_id is None and sender_id is None:
            logger.warn("on_reply: Both recipient and sender is None (admin)")
            return
        message = Message(
            session_id=session.id,
            profile_id=profile_id,
            recipient_id=recipient_id,
            sender_id=sender_id,
            content=raw_msg["content"],
            role=raw_msg["role"],
        )
        logger.debug(f"on_reply: {message}")

        db.post_message(message)

    crew = Crew(profile_id, session, composition, on_reply)

    background_tasks.add_task(crew.run, message, messages=cached_messages)

    return {"status": "success", "data": {"session": session.model_dump()}}


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
