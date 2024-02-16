from fastapi import FastAPI

from .dummy_maeve import composition
from .maeve import Maeve

app = FastAPI()


@app.get("/v0.0.0/run")
def run_autogen(maeve_id: str):
    maeve = Maeve("gpt-4-turbo-preview", composition=composition)

    maeve.run("Plan and improve the github repository https://github.com/Futino/futino")
