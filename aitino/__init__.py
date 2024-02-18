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


@app.get("/run")
def run_autogen(maeve_id: str):
    try:
        response = (
            supabase.table("maeve_nodes").select("*").eq("id", maeve_id).execute()
        )
    except Exception as e:
        return {"Error Getting Maeve: ": str(e)}

    prompt, composition = parse_input(response.data[0])
    return {"prompt": prompt, "composition": composition}
