from typing import Any, Protocol


class HttpClient(Protocol):
    async def post(
        self, url: str, json: dict[Any, Any], headers: dict[Any, Any]
    ) -> dict[Any, Any]: ...
