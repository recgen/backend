from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from health_backend.adapters.persistence.db import start_all_mappings
from health_backend.main.config import APIConfig
from health_backend.main.di import make_http_container
from health_backend.presentation.web_api import v2


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_all_mappings()
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    container = make_http_container()
    config = container.get_sync(APIConfig)

    setup_dishka(container, app)

    v2.include_routers(app)
    v2.include_error_handlers(app)
    v2.add_cors_middleware(app, config.origins)
    return app


def main() -> FastAPI:
    app = create_app()
    return app
