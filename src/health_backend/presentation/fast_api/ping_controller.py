from fastapi import APIRouter, status
from fastapi.routing import JSONResponse


class PingController:
    def __init__(self) -> None:
        self.router = APIRouter(prefix='/healthcheck', tags=['healthcheck'])
        self._register_routes()

    def _register_routes(self) -> None:
        @self.router.get('/ping')
        async def ping() -> JSONResponse:
            return JSONResponse(content={'message': 'pong'}, status_code=status.HTTP_200_OK)
