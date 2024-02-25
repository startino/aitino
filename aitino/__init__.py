import asyncio
import json
import logging
import os
import threading
from asyncio import Queue
from pathlib import Path
from typing import Any, AsyncGenerator, Generator, Literal
from uuid import UUID, uuid4

from autogen import Agent, ConversableAgent
from dotenv import load_dotenv
from fastapi import (
    BackgroundTasks,
    FastAPI,
    HTTPException,
    Response,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from pydantic import BaseModel
from starlette.responses import ContentStream
from starlette.types import Send
from supabase import Client, create_client

from .improver import PromptType, improve_prompt
from .maeve import Composition, Maeve
from .parser import parse_input

load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

supabase: Client = create_client(url, key)

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

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <div id='messages'>
        </div>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('p')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/test/chat")
def load_html():
    return HTMLResponse(html)


@app.get("/compile")
def compile(maeve_id: str) -> dict[str, str | Composition]:
    try:
        response = (
            supabase.table("maeve_nodes").select("*").eq("id", maeve_id).execute()
        )
    except Exception as e:
        return {"error": "could not fetch composition, error: " + str(e)}

    message, composition = parse_input(response.data[0])

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


class Reply(BaseModel):
    id: int
    status: Literal["success"] | Literal["error"] = "success"
    data: Any


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
                    Reply(id=i, status="success", data="done").model_dump()
                ) + "\n"
                break

            yield json.dumps(Reply(id=i, data=next_item).model_dump()) + "\n"
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
        # Runs Maeve (started in a separate thread)
        response = (
            supabase.table("maeve_nodes").select("*").eq("id", maeve_id).execute()
        )

        if len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Item not found")

        input = response.data[0]

        try:
            message, composition = parse_input(input)
            maeve = Maeve(composition, on_reply)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error: " + str(e))

        await maeve.run(message)
        await q.put(job_done)

    # Start the separate thread for running the maeve and adding items to the queue
    asyncio.run_coroutine_threadsafe(
        start_maeve(id),
        asyncio.get_event_loop(),
    )

    return StreamingResponse(watch_queue(), media_type="application/x-ndjson")
