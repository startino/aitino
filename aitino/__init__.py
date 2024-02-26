import asyncio
import json
import logging
import os
from asyncio import Queue
from pathlib import Path
from typing import Any, AsyncGenerator, cast
from uuid import UUID

from autogen import Agent, ConversableAgent
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import BaseModel

from .improver import PromptType, improve_prompt
from .interfaces import db
from .maeve import Composition, Maeve
from .models import StreamReply, Session, Message

logger = logging.getLogger("root")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:8001",
        "http://localhost:8081",
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


@app.get("/maeve")
async def run_maeve(id: UUID, session_id: UUID | None = None) -> StreamingResponse:
    q: Queue[Message | object] = Queue()
    job_done = object()

    # Get or create session
    session = None
    if session_id:
        session = db.get_session(session_id)
    if session is None:
        session = Session()

    async def watch_queue() -> AsyncGenerator:
        # Watch the queue and yield items (messages) as they arrive
        i = 0
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
        # This function is called when an LLM model replies
        if not messages:
            return
        if len(messages) == 0:
            return
        if not messages[-1].get("name"):
            return

        logger.info(f"on_reply: {recipient.name} {messages[-1]}")
        await q.put(
            Message(
                session_id=session.id,
                recipient=recipient.name,
                name=messages[-1]["name"],
                content=messages[-1]["content"],
                role=messages[-1]["role"],
            )
        )

    message, composition = db.get_complied(id)

    if not message or not composition:
        return StreamingResponse(
            json.dumps(
                StreamReply(
                    id=0,
                    status="error",
                    data=f"Maeve with id {id} not found",
                ).model_dump(),
                default=str,
            ),
            media_type="application/x-ndjson",
        )

    maeve = Maeve(composition, on_reply)

    # "maeve.run(message)" is run in a seperate thread
    asyncio.run_coroutine_threadsafe(
        maeve.run(message),
        asyncio.get_event_loop(),
    )

    return StreamingResponse(watch_queue(), media_type="application/x-ndjson")
