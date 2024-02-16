from fastapi import FastAPI

from .dummy_maeve import composition
from .maeve import Maeve

import os

# from supabase import create_client, Client
#
# url: str | None = os.environ.get("SUPABASE_URL")
# key: str | None = os.environ.get("SUPABASE_ANON_KEY")
#
# if url is None or key is None:
#     raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
#
# supabase: Client = create_client(url, key)

app = FastAPI()


@app.get("/v0.0.1/run")
def run_autogen(maeve_id: str):
    # response = supabase.table("maeve_nodes").select("*").eq("id", maeve_id)

    maeve = Maeve("gpt-4-turbo-preview", composition=composition)

    maeve.run("Plan and improve the github repository https://github.com/Futino/futino")
