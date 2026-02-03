from dataclasses import dataclass
from typing import Protocol

from health_backend.application.recommendation.dto import RecommendationDTO, ThresholdsDTO


class GeneratorService(Protocol):
    async def generate(self, patient_history: str) -> ThresholdsDTO: ...


@dataclass(frozen=True, slots=True)
class ThresholdsGenerator:
    service: GeneratorService

    async def generate(self, patient_history: str) -> ThresholdsDTO:
        return await self.service.generate(patient_history)
