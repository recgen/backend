from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from health_backend.domain.patient.entity import PatientId
from health_backend.domain.recommendation.entity import Recommendation
from health_backend.domain.recommendation.repository import RecommendationRepository


@dataclass(frozen=True, slots=True)
class SARecommendationRepository(RecommendationRepository):
    session: AsyncSession

    async def add(self, recommendation: Recommendation) -> None:
        self.session.add(recommendation)
        await self.session.flush()

    async def get_paginated(
        self, patient_id: PatientId, page: int, size: int
    ) -> tuple[list[Recommendation], int]:
        q = (
            select(Recommendation, func.count().over().label('total'))
            .where(Recommendation.patient_id == patient_id)  # ty: ignore
            .offset((page - 1) * size)
            .limit(size)
        )
        result = await self.session.execute(q)
        rows = result.all()
        if not rows:
            return [], 0
        recommendations, total = [row[0] for row in rows], rows[0][1]
        return recommendations, total
