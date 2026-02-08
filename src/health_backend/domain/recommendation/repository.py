from abc import abstractmethod
from typing import Protocol

from health_backend.domain.recommendation.entity import Recommendation


class RecommendationRepository(Protocol):
    @abstractmethod
    async def get_paginated(self, page: int, size: int) -> tuple[list[Recommendation], int]: ...
