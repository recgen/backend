from dataclasses import dataclass

from health_backend.application.common.errors import NotFound, Unauthorized
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.application.recommendation.dto import (
    PaginatedRecommendationsResponse,
    RecommendationDTO,
)
from health_backend.domain.patient.entity import PatientId
from health_backend.domain.patient.repository import PatientRepository
from health_backend.domain.recommendation.repository import RecommendationRepository


@dataclass(frozen=True, slots=True)
class GetPaginatedRecommendationsForPatient:
    idp: DoctorIdProvider
    patient_repo: PatientRepository
    recommendation_repo: RecommendationRepository

    async def execute(
        self, patient_id: PatientId, page: int, size: int
    ) -> PaginatedRecommendationsResponse:
        doctor_id = self.idp.get_id()
        if doctor_id is None:
            raise Unauthorized
        patient = await self.patient_repo.get_by_id(patient_id)
        if patient is None:
            raise NotFound
        recommendations, total = await self.recommendation_repo.get_paginated(page, size)
        return PaginatedRecommendationsResponse(
            recommendations=[RecommendationDTO.from_entity(rec) for rec in recommendations],
            page=page,
            size=size,
            total=total,
        )
