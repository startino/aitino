import asyncio
import json
import logging
import os
from asyncio import Queue
from pathlib import Path
from typing import Any, AsyncGenerator
from uuid import UUID

from autogen import Agent, ConversableAgent
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, StreamingResponse
from pydantic import BaseModel

from .improver import PromptType, improve_prompt
from .interfaces import db
from .maeve import Composition, Maeve
from .models import APIReply

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
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/compile")
def compile(id: UUID) -> dict[str, str | Composition]:
    message, composition = db.get_complied(id)

    return {"prompt": message, "composition": composition}


@app.get("/improve")
def improve(
    word_limit: int, prompt: str, temperature: float, prompt_type: PromptType
) -> str:
    return improve_prompt(word_limit, prompt, temperature, prompt_type)


class AgentReply(BaseModel):
    recipient: str
    sender: str | None = None
    message: str


@app.get("/maeve")
async def run_maeve(id: UUID):
    q: Queue[AgentReply | object] = Queue()
    job_done = object()

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
                    APIReply(id=i, status="success", data="done").model_dump()
                ) + "\n"
                break

            yield json.dumps(APIReply(id=i, data=next_item).model_dump()) + "\n"
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

        await q.put(
            AgentReply(
                recipient=recipient.name,
                sender=sender.name if sender else None,
                message=messages[-1]["content"],
            )
        )

    async def start_maeve(maeve_id: UUID):
        message, composition = db.get_complied(maeve_id)
        maeve = Maeve(composition, on_reply)
        await maeve.run(message)
        await q.put(job_done)

    # Start the separate thread for running the maeve and adding items to the queue
    asyncio.run_coroutine_threadsafe(
        start_maeve(id),
        asyncio.get_event_loop(),
    )

    return StreamingResponse(watch_queue(), media_type="application/x-ndjson")
