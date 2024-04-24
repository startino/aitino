import logging

from fastapi import APIRouter

router = APIRouter(
    prefix="/daniel",
    tags=["daniel"],
)

logger = logging.getLogger("root")


@router.get("/")
def read_sub():
    return {"message": "Hello World from sub API"}
