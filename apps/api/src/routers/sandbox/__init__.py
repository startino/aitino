import logging
from uuid import UUID

from fastapi import APIRouter, Depends, FastAPI, HTTPException

from . import (
    index,
    daniel,
    leon,
)


def create_app():
    app = FastAPI()
    app.include_router(index.router)
    app.include_router(daniel.router)
    app.include_router(leon.router)

    return app
