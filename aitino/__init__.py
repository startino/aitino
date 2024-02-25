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
    message: str
    sender: str | None = None


class Reply(BaseModel):
    id: int
    status: Literal["success"] | Literal["error"] = "success"
    data: Any


@app.get("/maeve")
async def run_maeve():
    q: Queue[AgentReply | object] = Queue(maxsize=1)
    job_done = object()

    async def iteration(i: int) -> Reply | Literal[False]:
        next_item = await q.get()

        q.task_done()

        # check if job is done
        if next_item is job_done or os.path.exists(Path(os.getcwd(), "STOP")):
            return False

        return Reply(id=i, data=next_item)

    async def generator() -> AsyncGenerator:
        for i in range(20):
            reply = await iteration(i)

            if not reply:
                break

            yield json.dumps(reply.model_dump()) + "\n"

    # START MAEVE
    async def on_reply(
        recipient: ConversableAgent,
        messages: list[dict] | None = None,
        sender: Agent | None = None,
        config: Any | None = None,
    ) -> None:
        logging.info("On reply")
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

    async def start_maeve():
        for i in range(10):
            reply = AgentReply(recipient="test", message="reply" + str(i))
            await q.put(reply)
            await asyncio.sleep(1)

    # Start the separate thread for adding items to the queue
    thread = threading.Thread(target=lambda: asyncio.run(start_maeve()))
    thread.start()

    # END MAEVE

    return StreamingResponse(generator(), media_type="application/x-ndjson")


# @app.get("/meave")
# async def run_maeve(maeve_id: UUID):
# logging.info("Running Maeve")
#
# q: Queue[AgentReply | object] = Queue(maxsize=1)
#
# async def on_reply(
#     recipient: ConversableAgent,
#     messages: list[dict] | None = None,
#     sender: Agent | None = None,
#     config: Any | None = None,
# ) -> None:
#     logging.info("On reply")
#     if not messages:
#         return
#     if len(messages) == 0:
#         return
#
#     print(messages[-1])
#     await q.put(
#         AgentReply(
#             recipient=recipient.name,
#             message=messages[0]["content"],
#             sender=sender.name if sender else None,
#         )
#     )
#     await q.join()
#
# async def run_job():
#     logging.info("Running job")
#     for i in range(10):
#         logging.info("Sending message")
#         await q.put(AgentReply(recipient="maeve", message="Hello"))
#         await asyncio.sleep(0.5)
#     await q.put(job_done)
#     response = (
#         supabase.table("maeve_nodes").select("*").eq("id", maeve_id).execute()
#     )
#
#     if len(response.data) == 0:
#         raise HTTPException(status_code=404, detail="Item not found")
#
#     input = response.data[0]
#
#     try:
#         message, composition = parse_input(input)
#         maeve = Maeve(composition, on_reply)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Error: " + str(e))
#
#     await q.put(await maeve.run(message))
#     await q.put(job_done)
#
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# thread = Thread(target=loop.run_until_complete, args=(run_job(),))
# thread.start()
# async def process(i: int) -> dict:
#     logging.info("Waiting for next item")
#     next_item = await q.get()
#     logging.info("Got next item")
#     if next_item is job_done or os.path.exists(Path(os.getcwd(), "STOP")):
#         return Reply(id=i, data="Done", last_message=True).model_dump()
#     q.task_done()
#     await asyncio.sleep(0.1)
#     logging.info("Done with item")
#     return Reply(id=i, data=next_item).model_dump()
#
# async def run_generator() -> AsyncGenerator:
#     logging.info("Running generator")
#     yield Reply(id=0, data="Starting").model_dump_json()
#     i = 1
#     for _ in range(100):
#         result = await process(i)
#         yield result
#         if result["last_message"]:
#             break

# return StreamingResponse(run_generator())
