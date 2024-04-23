import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="",
    tags=["sandbox"],
)

logger = logging.getLogger("root")


@router.get("/")
def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/sandbox/docs")


@router.get("/hello")
def read_sub():
    return {"message": "Hello World from sub API"}
