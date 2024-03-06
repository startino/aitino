import re
import asyncio
import logging
from typing import Any
from uuid import UUID

import autogen
from autogen import Agent, ConversableAgent
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .autobuilder import build_agents
from .crew import Crew
from .improver import PromptType, improve_prompt
from .interfaces import db
from .models import Message, Session, Composition

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
        "http://aiti.no",
        "http://api.aiti.no",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/compile")
def compile(id: UUID) -> dict[str, str | Composition]:
    message, composition = db.get_complied(id)

    return {
        "prompt": message if message else "Not Found",
        "composition": composition if composition else "Not Found",
    }


@app.get("/improve")
def improve(
    word_limit: int, prompt: str, prompt_type: PromptType, temperature: float
) -> str:
    return improve_prompt(word_limit, prompt, prompt_type, temperature)


@app.get("/crew")
async def run_crew(
    id: UUID, profile_id: UUID, session_id: UUID | None = None, reply: str | None = None
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

    message, composition = db.get_complied(id)

    if reply:
        message = reply

    if not message or not composition:
        raise HTTPException(status_code=400, detail=f"Crew with id {id} not found")

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
            logger.error("on_reply: No name")
            return
        if not raw_msg.get("content"):
            logger.error("on_reply: No content")
            return
        if not raw_msg.get("role"):
            logger.error("on_reply: No role")
            return

        def get_name_and_job_title(input_string):
            # Use regular expressions to insert spaces in camelCase and replace hyphens
            formatted_string = re.sub(r"([a-z])([A-Z])", r"\1 \2", input_string)
            formatted_string = re.sub(
                r"([A-Z])([A-Z][a-z])", r"\1 \2", formatted_string
            )
            formatted_string = formatted_string.replace("-", " - ")

            # Split the formatted string into name and job title
            name, job_title = map(str.strip, formatted_string.split(" - "))

            return name, job_title

        if get_name_and_job_title(raw_msg["name"])[0] not in [
            agent.name for agent in composition.agents
        ]:
            logger.error(f"on_reply: sender {raw_msg['name']} not in composition")
            return

        if get_name_and_job_title(recipient.name)[1] not in [
            agent.name for agent in composition.agents
        ]:
            logger.error(f"on_reply: recipient {recipient.name} not in composition")
            return

        logger.info(f"on_reply: {recipient.name} {raw_msg}")

        for agent in composition.agents:
            if agent.name == recipient.name:
                recipient_id = agent.id
            if agent.name == raw_msg["name"]:
                sender_id = agent.id

        message = Message(
            session_id=session.id,
            recipient_id=recipient_id,
            sender_id=sender_id,
            content=raw_msg["content"],
            role=raw_msg["role"],
        )

        db.post_message(message)

    crew = Crew(composition, on_reply)

    # "crew.run(message)" is run in a seperate thread
    asyncio.run_coroutine_threadsafe(
        crew.run(message, messages=cached_messages),
        asyncio.get_event_loop(),
    )

    return {"status": "success", "data": {"session_id": session.id}}


@app.get("/auto-build")
def auto_build_maeve(general_task: str):  # return maeve so maeve_run can run it
    agents = build_agents.BuildAgents()
    auto_build_agent = agents.create_all_in_one_agent()
    # task_simplifier = agents.create_task_simplifier(general_task)
    # agent_employer = agents.create_employer()
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        system_message="test admin",
        code_execution_config=False,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
    )
    user_proxy.initiate_chat(
        auto_build_agent,
        message=general_task,
    )
