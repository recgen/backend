import uvicorn
from fastapi import FastAPI

from health_backend.presentation.fast_api.ping_controller import PingController


def include_routers(app: FastAPI) -> None:
    app.include_router(PingController().router)


def run() -> None:
    uvicorn.run(
        create_app(),
        host='127.0.0.1',
        port=6969,
    )


def create_app() -> FastAPI:
    app = FastAPI()
    include_routers(app)
    return app


if __name__ == '__main__':
    run()
