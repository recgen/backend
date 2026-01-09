from fastapi import FastAPI

from health_backend.presentation.web_fastapi.routes import healthcheck


def create_app() -> FastAPI:
    app = FastAPI()
    include_routers(app)
    return app


def include_routers(app: FastAPI) -> None:
    app.include_router(healthcheck.router)
