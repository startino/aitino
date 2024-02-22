import json
import logging
import os

from typing import Literal
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from supabase import Client, create_client

from .cache_service import CacheService
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


@app.get("/cache/{seed}")
def get_cache(seed: int) -> dict:
    try:
        cache_service = CacheService(seed)

        return {"cache": cache_service.poll_cache()}
    except Exception as e:
        return {"error": "could not fetch cache, error: " + str(e)}


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


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    try:
        while True:

            async def on_message(message: str, websocket: WebSocket):
                await manager.send_personal_message(
                    f"Message text was: {message}", websocket
                )

            maeve_id = await websocket.receive_text()
            _ = CacheService(41)
            await manager.send_personal_message(f"You ran: {maeve_id}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {maeve_id}")
            try:
                response = (
                    supabase.table("maeve_nodes")
                    .select("*")
                    .eq("id", maeve_id)
                    .execute()
                ).data[0]
            except Exception as e:
                error = {"error": "could not fetch composition, error: " + str(e)}
                await manager.send_personal_message(f"{error}", websocket)
                continue

            try:
                message, composition = parse_input(response)
                maeve = Maeve(composition, on_message, websocket)
            except Exception as e:
                error = {"error": "couldn't create maeve: " + str(e)}
                await manager.send_personal_message(f"{error}", websocket)
                continue

            await manager.send_personal_message(
                f"Running with details:\nMaeve: {maeve_id}\nPrompt: {message}",
                websocket,
            )
            await maeve.run(message)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
