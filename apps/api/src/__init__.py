import asyncio
import json
import logging
import os
import autogen

from asyncio import Queue
from pathlib import Path
from typing import Any, AsyncGenerator, cast
from uuid import UUID

from autogen import Agent, ConversableAgent
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from openai import OpenAI


from .improver import PromptType, improve_prompt
from .interfaces import db
from .crew import Composition, Crew
from .models import StreamReply, Session, Message
from .autobuilder import build_agents
 

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
) -> StreamingResponse:
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

    q: Queue[Message | object] = Queue()
    job_done = object()

    async def watch_queue() -> AsyncGenerator:
        # Watch the queue and yield items (messages) as they arrive
        i = 0

        # Yield session
        yield json.dumps(
            StreamReply(id=i, data={"session_id": str(session.id)}).model_dump(),
            default=str,
        ) + "\n"

        i += 1

        while True:
            # Gets and dequeues item
            next_item = await q.get()

            # check if job is done or if it should be force stopped
            if (
                next_item is job_done
                or os.path.exists(Path(os.getcwd(), "STOP"))
                or i == 1000  # failsafe because while True scary
            ):
                yield json.dumps(
                    StreamReply(id=i, status="success", data="done").model_dump(),
                    default=str,
                ) + "\n"
                break

            yield json.dumps(
                StreamReply(id=i, data=next_item).model_dump(), default=str
            ) + "\n"
            i += 1

    async def on_reply(
        recipient: ConversableAgent,
        messages: list[dict] | None = None,
        sender: Agent | None = None,
        config: Any | None = None,
    ) -> None:
        logger.debug(f"on_reply: {recipient.name} {messages}")
        # This function is called when an LLM model replies
        if not messages:
            return
        if len(messages) == 0:
            return
        if not messages[-1].get("name"):
            return

        logger.info(f"on_reply: {recipient.name} {messages[-1]}")
        message = Message(
            session_id=session.id,
            recipient=recipient.name,
            name=messages[-1]["name"],
            content=messages[-1]["content"],
            role=messages[-1]["role"],
        )
        db.post_message(message)
        await q.put(message)

    crew = Crew(composition, on_reply)

    # "crew.run(message)" is run in a seperate thread
    asyncio.run_coroutine_threadsafe(
        crew.run(message, messages=cached_messages, q=q, job_done=job_done),
        asyncio.get_event_loop(),
    )

    return StreamingResponse(watch_queue(), media_type="application/x-ndjson")

@app.get("/auto-build")
def auto_build_maeve(
    general_task: str, profile_id: UUID
    ): #return maeve so maeve_run can run it
        agents = build_agents.BuildAgents()
        auto_build_agent = agents.create_all_in_one_agent()
        #task_simplifier = agents.create_task_simplifier(general_task)
        #agent_employer = agents.create_employer()
        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            system_message="test admin",
            code_execution_config=False,
            human_input_mode="NEVER",
            default_auto_reply="Reply TERMINATE if the task has been solved at full satisfaction. If you instead require more information reply TERMINATE along with a list of items of information you need. Otherwise, reply CONTINUE, or the reason why the task is not solved yet.",
            max_consecutive_auto_reply=1
        )
        chat_result = user_proxy.initiate_chat(
            auto_build_agent,
            message=general_task,
            silent=True
        )
        crew_frame = chat_result.chat_history[1]["content"]
        print(crew_frame)
        return (crew_frame)
        #some_comp = some_json_parser_and_comp_creator(crew_frame) 

        #client = OpenAI()

@app.get("/test")
def rate_limit(profile_id: )