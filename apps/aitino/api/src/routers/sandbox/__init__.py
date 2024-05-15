from fastapi import FastAPI

from . import daniel, index, leon


def create_app():
    app = FastAPI()
    app.include_router(index.router)
    app.include_router(daniel.router)
    app.include_router(leon.router)

    return app
