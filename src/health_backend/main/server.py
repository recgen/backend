from contextlib import asynccontextmanager

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from health_backend.main.config import config
from health_backend.main.di import container
from health_backend.presentation.web_api import v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    setup_dishka(container, app)
    v1.include_routers(app)
    v1.include_error_handlers(app)
    v1.add_cors_middleware(app, [config.frontend_origin])
    return app


def main() -> None:
    app = create_app()
    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
    )
