import json
import logging
import os
from typing import Literal
from uuid import UUID

from dotenv import load_dotenv
from pydantic import ValidationError
from supabase import Client, create_client
from praw.models import Submission

from src.rest import reddit_utils
from src.rest.models.evaluated_submission import EvaluatedSubmission

from ..models import Lead
from datetime import datetime, timedelta

load_dotenv()

url: str | None = os.environ.get("REST_SUPABASE_URL")
key: str | None = os.environ.get("REST_SUPABASE_ANON_KEY")

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
    logger.debug(f"Posting lead: {lead}")
    supabase.table("leads").insert(
        json.loads(json.dumps(lead.model_dump(), default=str))
    ).execute()


def update_lead(id: UUID, status: str = "", last_event: str = "") -> None:
    """
    Update a lead in the database.
    """
    # Create a dictionary with only non-empty values
    data = {k: v for k, v in {"status": status, "last_event": last_event}.items() if v}

    logger.debug(f"Updating lead with data: {data}")
    supabase.table("leads").update(data).eq("id", str(id)).execute()


def post_submission(submission: EvaluatedSubmission):
    """
    Post a submission to the database.
    """
    logger.debug(f"Posting submission: {submission}")
    supabase.table("submissions").insert(
        json.loads(json.dumps(submission.model_dump(), default=str))
    ).execute()


if __name__ == "__main__":
    reddit = reddit_utils.get_reddit_instance(
        username="antopia_hk", password="jorge-loves-donuts-eh-?!"
    )
    test_submission = reddit.submission("n9o4l3")
    post_submission(
        EvaluatedSubmission(
            submission=test_submission,
            is_relevant=True,
            cost=0.0,
            reason="test",
            qualifying_question="test",
        )
    )
