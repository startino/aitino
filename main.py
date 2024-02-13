import json

import autogen
from fastapi import FastAPI

from maeve import Maeve

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/run")
def run_autogen():
    with open("maeve.json", "r") as file:
        data = json.load(file)

    maeve = Maeve("gpt-4-turbo-preview", composition=data)

    maeve.run(
        "Come up with suggestions to improve the github repository https://github.com/Futino/futino"
    )
