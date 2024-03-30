import json
import logging
import os
from typing import Literal
from uuid import UUID

from dotenv import load_dotenv
from pydantic import ValidationError
from supabase import Client, create_client

from models import Lead
from datetime import datetime, timedelta

load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")

supabase: Client = create_client(url, key)

logger = logging.getLogger("root")


def get_lead(lead_id: UUID) -> Lead | None:
    """
    Get a lead from the database.
    """
    logger.debug(f"Getting lead: {lead_id}")
    response = supabase.table("leads").select("*").eq("id", str(lead_id)).execute()
    
    if len(response.data) == 0:
        return None
    return Lead(**response.data[0])

def get_due_leads(due_after_days: int = 3) -> list[Lead] | None:
    """
    Get leads that are due for a follow-up.
    """
    logger.debug("Getting due leads")

    date = datetime.now() - timedelta(days=due_after_days)

    response = supabase.table("leads").select("*").neq("status", "dead").lt("last_contacted_at", date).execute()
    
    leads = []

    try:
        leads = [Lead(**lead) for lead in response.data]
    except ValidationError as e:
        logger.error(f"Error validating lead: {e}")
    
    return leads


def post_lead(lead: Lead) -> None:
    """
    Post a lead to the database.
    """
    logger.debug(f"Posting lead: {lead}")
    supabase.table("leads").insert(
        json.loads(json.dumps(lead.model_dump(), default=str))
    ).execute()



if __name__ == '__main__':
   

    lead = Lead(
        redditor="u/antopia_hk",
        source="Reddit",
        last_event="Contacted",
        title="Hello",
        body="Hello, I am interested in your product.")
    post_lead(lead)
    lead = get_lead(lead.id)
    print(lead)