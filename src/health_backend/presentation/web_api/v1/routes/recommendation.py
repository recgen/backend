from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from health_backend.application.recommendation.dto import GenerateRecommendationResponse
from health_backend.application.recommendation.generate import GenerateRecommendation
from health_backend.domain.patient.entity import PatientId
from health_backend.presentation.web_api.v1.schemas.recommendation import (
    GenerateRecommendationRequest,
)

router = APIRouter(
    tags=['Recommendation'],
    prefix='/recommendation',
    route_class=DishkaRoute,
)


@router.post('/')
async def create_recommendation(
    request: GenerateRecommendationRequest,
    use_case: FromDishka[GenerateRecommendation],
) -> GenerateRecommendationResponse:
    return await use_case.execute(
        patient_id=PatientId(request.patient_id),
        patient_history=request.patient_history,
    )
