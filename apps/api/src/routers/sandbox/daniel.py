import logging
from fastapi import FastAPI

from fastapi import APIRouter, Depends, HTTPException

daniel = FastAPI()

router = APIRouter(
    prefix="/daniel",
    tags=["daniel"],
)

logger = logging.getLogger("root")


@router.get("/")
def read_sub():
    return {"message": "Hello World from sub API"}
