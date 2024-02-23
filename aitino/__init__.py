import asyncio
import json
import logging
import os
from asyncio import Queue
from pathlib import Path
from threading import Thread
from typing import Any, AsyncGenerator, Literal
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
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from starlette.types import Send
from supabase import Client, create_client

from .improver import improve_prompt
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


@app.get("/testing/chat")
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
    word_limit: int,
    prompt: str,
    prompt_type: Literal["generic", "system", "user"] = "generic",
) -> str:
    return improve_prompt(word_limit, prompt, prompt_type)


class AgentReply(BaseModel):
    recipient: str
    message: str
    sender: str | None = None


class Reply(BaseModel):
    id: int
    data: Any
    last_message: bool = False


@app.get("/meave")
async def run_maeve(maeve_id: UUID):
    job_done = object()

    q: Queue[AgentReply | object] = Queue(maxsize=1)

    async def on_reply(
        recipient: ConversableAgent,
        messages: list[dict] | None = None,
        sender: Agent | None = None,
        config: Any | None = None,
    ) -> None:
        if not messages:
            return
        if len(messages) == 0:
            return

        print(messages[-1])
        await q.put(
            AgentReply(
                recipient=recipient.name,
                message=messages[0]["content"],
                sender=sender.name if sender else None,
            )
        )
        await q.join()

    async def run_job():
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

        await q.put(await maeve.run(message))
        await q.put(job_done)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    thread = Thread(target=loop.run_until_complete, args=(run_job(),))
    thread.start()

    async def run_generator() -> AsyncGenerator:
        yield Reply(id=0, data="Starting")
        i = 1
        while True:
            next_item = q.get()
            if next_item is job_done or os.path.exists(Path(os.getcwd(), "STOP")):
                yield Reply(id=i, data="Done", last_message=True)
                break
            yield Reply(id=i, data=next_item)
            q.task_done()

    return StreamingResponse(run_generator())
