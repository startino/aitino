from fastapi import FastAPI

from .parser import parse_input
from .maeve import Maeve
from dotenv import load_dotenv

import os

from supabase import create_client, Client

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


@app.get("/run")
def run(maeve_id: str):
    try:
        response = (
            supabase.table("maeve_nodes").select("*").eq("id", maeve_id).execute()
        )
    except Exception as e:
        return {"error": "could not fetch composition, error: " + str(e)}

    message, composition = parse_input(response.data[0])

    try:
        maeve = Maeve(composition)
    except Exception as e:
        return {"error": str(e)}

    result = maeve.run(message)

    return {"prompt": message, "composition": composition, "result": result}
