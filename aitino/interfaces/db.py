import logging
import os
from uuid import UUID

from dotenv import load_dotenv
from supabase import Client, create_client

from ..maeve import Composition
from ..parser import parse_input

load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

supabase: Client = create_client(url, key)

logger = logging.getLogger("root")


def get_complied(id: UUID) -> tuple[str, Composition] | tuple[None, None]:
    response = supabase.table("maeve_nodes").select("*").eq("id", id).execute()

    if len(response.data) == 0:
        return None, None

    return parse_input(response.data[0])
