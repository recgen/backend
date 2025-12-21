import uvicorn
from fastapi import FastAPI

from health_backend.bootstrap.config import config
from health_backend.presentation.fast_api.ping_controller import PingController


def include_routers(app: FastAPI) -> None:
    app.include_router(PingController().router)


def run() -> None:
    uvicorn.run(
        create_app(),
        host=config.host,
        port=config.port,
    )


def create_app() -> FastAPI:
    app = FastAPI()
    include_routers(app)
    return app


if __name__ == '__main__':
    run()
