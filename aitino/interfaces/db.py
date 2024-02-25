from ..maeve import Composition
from ..parser import parse_input
from fastapi import HTTPException
import supabase
from uuid import UUID


def get_composition(id: UUID) -> tuple[str, Composition]:
    response = supabase.table("maeve_nodes").select("*").eq("id", id).execute()

    if len(response.data) == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return parse_input(response.data[0])
