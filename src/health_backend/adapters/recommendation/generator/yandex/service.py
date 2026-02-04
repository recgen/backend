import json
from dataclasses import dataclass, field
from typing import Any

from health_backend.adapters.common.http.client import HttpClient
from health_backend.adapters.recommendation.generator.common.request_builder import RequestBuilder
from health_backend.adapters.recommendation.generator.common.response_parser import ResponseParser
from health_backend.application.recommendation.dto import ThresholdsDTO
from health_backend.application.recommendation.generator import GeneratorService


@dataclass(frozen=True, slots=True)
class YandexGPTGeneratorService(GeneratorService):
    api_url: str
    http_client: HttpClient
    request_builder: RequestBuilder
    response_parser: ResponseParser

    async def generate(self, patient_history: str) -> ThresholdsDTO:
        body = self.request_builder.body(patient_history)
        headers = self.request_builder.headers()
        response = await self.http_client.post(
            url=self.api_url,
            json=body,
            headers=headers,
        )
        return self.response_parser.parse(response)
