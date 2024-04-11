import json
import logging
import os
from typing import Literal
from uuid import UUID

from dotenv import load_dotenv
from pydantic import ValidationError
from supabase import Client, create_client

from models import Lead, PublishCommentResponse
from datetime import datetime, timedelta

from models import EvaluatedSubmission
from models import SavedSubmission

load_dotenv()

url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_ANON_KEY")

if url is None or key is None:
    raise ValueError("REST_SUPABASE_URL and REST_SUPABASE_ANON_KEY must be set")


logger = logging.getLogger("root")


def get_lead(lead_id: UUID) -> Lead | None:
    """
    Get a lead from the database.
    """
    supabase: Client = create_client(url, key)
    logger.debug(f"Getting lead: {lead_id}")
    response = supabase.table("leads").select("*").eq("id", str(lead_id)).execute()

    if len(response.data) == 0:
        return None
    return Lead(**response.data[0])


def get_due_leads(due_after_days: int = 3) -> list[Lead] | None:
    """
    Get leads that are due for a follow-up.
    """
    supabase: Client = create_client(url, key)
    logger.debug("Getting due leads")

    date = datetime.now() - timedelta(days=due_after_days)

    response = (
        supabase.table("leads")
        .select("*")
        .neq("status", "dead")
        .lt("last_contacted_at", date)
        .execute()
    )

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
    supabase: Client = create_client(url, key)
    logger.debug(f"Posting lead: {lead}")
    supabase.table("leads").insert(
        json.loads(json.dumps(lead.model_dump(), default=str))
    ).execute()


def update_lead(
    id: UUID, status: str = "", last_event: str = ""
) -> PublishCommentResponse:
    """
    Update a lead in the database.
    """
    supabase: Client = create_client(url, key)
    # Create a dictionary with only non-empty values
    data = {k: v for k, v in {"status": status, "last_event": last_event}.items() if v}

    logger.debug(f"Updating lead with data: {data}")
    response = supabase.table("leads").update(data).eq("id", str(id)).execute()
    # returns the updated object, as a pydantic object
    return PublishCommentResponse(**response.data[0])


def get_all_leads() -> list[PublishCommentResponse]:
    supabase: Client = create_client(url, key)
    response = supabase.table("leads").select("*").execute()
    return [PublishCommentResponse(**data) for data in response.data]


def update_human_review_for_submission(id: UUID, human_answer: bool) -> None:
    """
    Update the human review for a submission.
    Just a shortcut to avoid double work as posts with published comments are
    already human reviewed.
    """
    supabase: Client = create_client(url, key)
    logger.debug(f"Updating human review for submission: {id}")
    supabase.table("evaluated_submissions").update({"human_answer": human_answer}).eq


def post_evaluated_submission(saved_submission: SavedSubmission) -> None:
    """
    Post a submission to the database.
    """
    supabase: Client = create_client(url, key)
    logger.debug(f"Posting submission: {saved_submission}")

    supabase.table("evaluated_submissions").insert(
        json.loads(json.dumps(saved_submission.model_dump(), default=str))
    ).execute()
