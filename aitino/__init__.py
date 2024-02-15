from fastapi import FastAPI

from .dummy_maeve import composition
from .maeve import Maeve

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/run")
def run_autogen():
    maeve = Maeve("gpt-4-turbo-preview", composition=composition)

    maeve.run("Plan and improve the github repository https://github.com/Futino/futino")
