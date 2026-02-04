from typing import Any, Protocol

from health_backend.application.recommendation.dto import ThresholdsDTO


class ResponseParser(Protocol):
    def parse(self, response: dict[Any, Any]) -> ThresholdsDTO: ...
