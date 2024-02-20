import os
import json

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
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

app = FastAPI()


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


def data_streamer(maeve_id: str):
    try:
        response = (
            supabase.table("maeve_nodes").select("*").eq("id", maeve_id).execute()
        )
    except Exception as e:
        return {"error": "could not fetch composition, error: " + str(e)}

    message, composition = parse_input(response.data[0])
    json.dumps({"event_id": 0, "data": message, "is_last_event": True})

    try:
        maeve = Maeve(composition)
    except Exception as e:
        return {"error": str(e)}

    result = maeve.run(message)
    yield json.dumps({"event_id": 1, "data": result, "is_last_event": True})


@app.get("/run")
async def run(maeve_id: str):

    return StreamingResponse(data_streamer(maeve_id), media_type="application/x-ndjson")


@app.get("/improve")
def improve(word_limit: int, prompt: str) -> str:

    return improve_prompt(word_limit, prompt)
