import logging
from fastapi import FastAPI

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(
    prefix="/autogen",
    tags=["autogen"],
)

logger = logging.getLogger("root")

daniel = FastAPI()


@daniel.get("/sub")
def read_sub():
    return {"message": "Hello World from sub API"}
