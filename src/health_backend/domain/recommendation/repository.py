from abc import abstractmethod
from typing import Protocol

from health_backend.domain.patient.entity import PatientId
from health_backend.domain.recommendation.entity import Recommendation


class RecommendationRepository(Protocol):
    @abstractmethod
    async def get_paginated(
        self, patient_id: PatientId, page: int, size: int
    ) -> tuple[list[Recommendation], int]: ...

    @abstractmethod
    async def add(self, recommendation: Recommendation) -> None: ...
