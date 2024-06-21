import logging
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from arxiv_utils import get_papers
from mail import email_articles

from relevance_bot import filter_papers

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
    papers = filter_papers(papers)
    print(papers.pdf_url)
    # email_articles(papers)
    return {"success": "true"}
