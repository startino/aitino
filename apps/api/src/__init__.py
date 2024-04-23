import logging
from uuid import UUID

import autogen
from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import uvicorn

from src.open_logger import configure_loggers
from src.routers import api_provider

from src import mock as mocks
from src.auth import get_current_user
from src.autobuilder import build_agents
from src.crew import AutogenCrew
from src.dependencies import (
    RateLimitResponse,
    rate_limit,
    rate_limit_profile,
    rate_limit_tiered,
)
from src.improver import PromptType, improve_prompt
from src.interfaces import db
from src.models import Profile
from src.routers import agents, api_provider, api_keys
from src.routers import auth as auth_router
from src.routers import (
    billing_information,
    crews,
    messages,
    profiles,
    rest,
    sessions,
    subscriptions,
    tiers,
    tools,
    index,
    sandbox,
)


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(index.router)
    app.include_router(sessions.router)
    app.include_router(messages.router)
    app.include_router(crews.router)
    app.include_router(agents.router)
    app.include_router(profiles.router)
    app.include_router(api_keys.router)
    app.include_router(auth_router.router)
    app.include_router(api_provider.router)
    app.include_router(tools.router)
    app.include_router(subscriptions.router)
    app.include_router(rest.router)
    app.include_router(tiers.router)
    app.include_router(billing_information.router)

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
            "https://aiti.no",
            "https://api.aiti.no",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


if __name__ == "__main__":
    app = create_app()
    sandbox_app = sandbox.create_app()
    app.mount("/sandbox", sandbox_app)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_config="logging.yaml")
