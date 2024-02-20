import os
import json
import time
import logging

from typing import Any
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, StreamingResponse
from supabase import Client, create_client

from .improver import improve_prompt
from .maeve import Maeve
from .parser import parse_input

load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

supabase: Client = create_client(url, key)

logger = logging.getLogger('root')

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
@app.get("/chat")
def load_html():
    return HTMLResponse(html)

@app.get("/compile")
def compile(maeve_id: str):
    try:
        response = (
            supabase.table("maeve_nodes").select("*").eq("id", maeve_id).execute()
        )
    except Exception as e:
        return {"error": "could not fetch composition, error: " + str(e)}

    message, composition = parse_input(response.data[0])

    return {"prompt": message, "composition": composition}


def callback_test(message: str) -> None:
    print(message)


async def data_streamer(maeve_id: str):
    try:
        response = (
            supabase.table("maeve_nodes").select("*").eq("id", maeve_id).execute()
        )
    except Exception as e:
        yield json.dumps({"error": "could not fetch composition, error: " + str(e)})
        return

    message, composition = parse_input(response.data[0])
    json.dumps({"event_id": 0, "data": message, "is_last_event": False})

    try:
        maeve = Maeve(composition, callback_test)
    except Exception as e:
        yield json.dumps({"error": "couldn't create maeve: " + str(e)})
        return

    maeve.run(message)

    for i in range(10):
        yield json.dumps({"event_id": i + 1, "data": f"Hello {i}", "is_last_event": False})
        time.sleep(1)

    yield json.dumps({"event_id": 11, "data": "", "is_last_event": True})


@app.get("/run")
async def run(maeve_id: str):

    return StreamingResponse(data_streamer(maeve_id), media_type="application/x-ndjson")


@app.get("/improve")
def improve(word_limit: int, prompt: str) -> str:

    return improve_prompt(word_limit, prompt)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async def on_message(message: str, websocket: WebSocket) -> None:
        await websocket.send_text(f"Message text was: {message}")

    try:
        response = (
            supabase.table("maeve_nodes").select("*").eq("id", "dfb9ede1-3c08-462f-af73-94cf6aa9185a").execute()
        )
    except Exception as e:
        logger.info(json.dumps({"error": "could not fetch composition, error: " + str(e)}))
        return

    message, composition = parse_input(response.data[0])
    maeve = Maeve(composition, on_message, websocket)
    try:
        logger.info(composition)
        
    except Exception as e:
        logger.info(json.dumps({"error": "couldn't create maeve: " + str(e)}))
        return
    
    maeve.run(message)