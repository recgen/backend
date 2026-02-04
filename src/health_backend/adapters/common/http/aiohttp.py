from typing import Any

import aiohttp

from health_backend.adapters.common.http.client import HttpClient


class AioHttpClient(HttpClient):
    async def post(self, url: str, json: dict[Any, Any], headers: dict[Any, Any]) -> dict[Any, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, json=json, headers=headers) as response:
                return await response.json()
