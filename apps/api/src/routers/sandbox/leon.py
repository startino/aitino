import logging

from fastapi import APIRouter

router = APIRouter(
    prefix="/leon",
    tags=["leon"],
)

logger = logging.getLogger("root")


@router.get("/")
def read_sub():
    return {"message": "Hello World from sub API"}
