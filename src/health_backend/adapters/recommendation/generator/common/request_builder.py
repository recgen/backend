from dataclasses import dataclass, field
from typing import Any, Protocol


class RequestBuilder(Protocol):
    def body(self, patient_history: str) -> dict[str, Any]: ...

    def headers(self) -> dict[str, Any]: ...
