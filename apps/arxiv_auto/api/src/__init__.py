import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import index

from arxiv_utils import get_papers
from relevance_bot import filter_papers


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(index.router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:8000",
            "http://localhost:8001",
            "http://localhost:8080",
            "http://localhost:8081",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "http://127.0.0.1:8000",
            "http://127.0.0.1:8001",
            "http://127.0.0.1:8080",
            "http://127.0.0.1:8081",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def run():
    app = create_app()

    uvicorn.run(app, host="0.0.0.0", port=5050, log_config="logging.yaml")


def api_replacement():
    papers = get_papers(
        "language model ai artificial intelligence machine learning agents cat:cs"
    )
    papers = filter_papers(papers)
    print(papers)
    # email_articles(papers)
    return {"success": "true"}


if __name__ == "__main__":
    api_replacement()
