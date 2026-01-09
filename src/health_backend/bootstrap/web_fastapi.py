import uvicorn
from fastapi import FastAPI

from health_backend.bootstrap.config import config
from health_backend.presentation.web_fastapi import create_app, include_routers


def run() -> None:
    uvicorn.run(
        create_app(),
        host=config.host,
        port=config.port,
    )


if __name__ == '__main__':
    run()
