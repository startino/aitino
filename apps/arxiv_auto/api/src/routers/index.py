import logging
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import os
from dotenv import load_dotenv
import threading
from uuid import uuid4

from src.interfaces import db

from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from arxiv_utils import get_papers
from mail import email_articles

load_dotenv()

router = APIRouter()


@router.get("/")
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@router.post("/main")
def main():
    papers = get_papers(
        "language model ai artificial intelligence machine learning agents cat:cs"
    )
    email_articles(papers)
    return {"success": "true"}
