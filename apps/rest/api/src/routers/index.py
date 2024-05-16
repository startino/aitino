import logging
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
import threading
from uuid import uuid4

from src.interfaces import db
from src import comment_bot
from src.models import PublishCommentRequest, GenerateCommentRequest, FalseLead, Lead
from src.reddit_worker import RedditStreamWorker
from src import upwork_worker

from fastapi import HTTPException
from fastapi.responses import RedirectResponse

# Relevant subreddits to Startino
SUBREDDIT_NAMES = (
    "SaaS+SaaSy+startups+YoungEntrepreneurs+NoCodeSaas+nocode+cofounder+Entrepreneur+futino"
)

load_dotenv()
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")

if REDDIT_PASSWORD is None:
    raise ValueError("REDDIT_PASSWORD is not set")

if REDDIT_USERNAME is None:
    raise ValueError("REDDIT_USERNAME is not set")

workers = {}

router = APIRouter()

@router.get("/")
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@router.get("/test")
def test():
    print("TEST")
    db.post_lead(
        Lead(
            id=uuid4(),
            submission_id=uuid4(),
            reddit_id="test",
            prospect_username="test",
            source="test",
            last_event="test",
            status="test",
            data={"test": "test"},
        )
    )


@router.post("/start")
def start_stream():
    worker_id = str(uuid4())
    worker = RedditStreamWorker(SUBREDDIT_NAMES, REDDIT_USERNAME, REDDIT_PASSWORD)
    thread = threading.Thread(target=worker.start)
    workers[worker_id] = (worker, thread)
    thread.start()
    return {"worker_id": worker_id}


@router.post("/stop/{worker_id}")
def stop_stream(worker_id: str):
    worker, thread = workers.get(worker_id, (None, None))
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    worker.stop()
    thread.join(timeout=10)  # Waits 10 seconds for the thread to finish

    if thread.is_alive():
        logging.error(f"Thread for Reddit worker didn't stop in time")

    del workers[worker_id]  # Cleanup

    return {"message": "Stream stopped"}


@router.post("/generate-comment")
def generate_comment(generate_request: GenerateCommentRequest):
    comment: str = comment_bot.generate_comment(
        generate_request.title,
        generate_request.selftext,
        generate_request.instructions
    )
    if comment is None:
        raise HTTPException(404, "comment not found")

    return comment


@router.post("/mark-lead-as-irrelevant")
def mark_lead_as_irrelevant(false_lead: FalseLead):
    # Mark the lead as irrelevant in 'leads' table
    lead = db.update_lead(id=false_lead.lead_id, status="rejected")

    if lead is None:
        raise HTTPException(404, "lead not found")

    # Mark the submission as irrelevant in 'evaluated_submissions' table as a
    # human answer and review
    db.update_human_review_for_submission(
        id=false_lead.submission_id,
        human_answer=False,
        correct_reason=false_lead.correct_reason,
    )

    return {"status": "success"}


@router.post("/publish-comment")
def publish_comment(publish_request: PublishCommentRequest):
    updated_content = comment_bot.publish_comment(
        publish_request.lead_id,
        publish_request.comment,
        publish_request.reddit_username,
        publish_request.reddit_password,
    )
    if updated_content is None:
        raise HTTPException(404, "lead not found")

    return updated_content


@router.get("/generate-proposal")
def generate_proposal(post: str):
    proposal = upwork_worker.generate_proposal(post)
    return proposal
