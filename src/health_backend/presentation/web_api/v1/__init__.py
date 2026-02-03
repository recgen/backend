from fastapi import FastAPI

from health_backend.presentation.web_api.v1.routes import recommendation


def include_routers(app: FastAPI) -> None:
    app.include_router(recommendation.router)
