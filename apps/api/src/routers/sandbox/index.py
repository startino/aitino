import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/sandbox",
    tags=["sandbox"],
)

logger = logging.getLogger("root")


@router.get("/")
def read_sub():
    return {"message": "Hello World from sub API"}
