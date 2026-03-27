from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from health_backend.application.recommendation.dto import (
    GenerateRecommendationForPatientResponse,
    PaginatedRecommendationsResponse,
)
from health_backend.application.recommendation.generate import GenerateRecommendationForPatient
from health_backend.application.recommendation.get import GetPaginatedRecommendationsForPatient
from health_backend.domain.patient.entity import PatientId
from health_backend.presentation.web_api.v2.schemas.recommendation import (
    GenerateRecommendationRequest,
)

router = APIRouter(
    tags=['Recommendation'],
    prefix='/recommendations',
    route_class=DishkaRoute,
)


@router.post('')
async def create_recommendation(
    request: GenerateRecommendationRequest,
    use_case: FromDishka[GenerateRecommendationForPatient],
) -> GenerateRecommendationForPatientResponse:
    return await use_case.execute(
        patient_id=PatientId(request.patient_id),
        patient_history=request.patient_history,
    )


@router.get('')
async def get_paginated_recommendations(
    use_case: FromDishka[GetPaginatedRecommendationsForPatient],
    patient_id: PatientId,
    page: int = 1,
    size: int = 20,
) -> PaginatedRecommendationsResponse:
    return await use_case.execute(patient_id, page, size)
