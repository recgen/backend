from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from health_backend.application.common.uow import UnitOfWork
from health_backend.application.recommendation.dto import (
    GenerateRecommendationResponse,
    RecommendationDTO,
    ThresholdsDTO,
)
from health_backend.application.recommendation.generator import ThresholdsGenerator
from health_backend.domain.common.vo import Range
from health_backend.domain.patient.entity import PatientId
from health_backend.domain.recommendation.entity import Recommendation
from health_backend.domain.recommendation.vo import Thresholds


@dataclass(frozen=True, slots=True)
class GenerateRecommendation:
    generator: ThresholdsGenerator
    # uow: UnitOfWork

    async def execute(
        self, patient_id: PatientId, patient_history: str
    ) -> GenerateRecommendationResponse:
        thresholds_dto = await self.generator.generate(patient_history)
        recommendation = Recommendation.create(
            patient_id,
            Thresholds(
                systolic_blood_pressure=Range.create(
                    thresholds_dto.systolic_blood_pressure_min,
                    thresholds_dto.systolic_blood_pressure_max,
                ),
                diastolic_blood_pressure=Range.create(
                    thresholds_dto.diastolic_blood_pressure_min,
                    thresholds_dto.diastolic_blood_pressure_max,
                ),
                temperature_celsius=Range.create(
                    thresholds_dto.temperature_celsius_min,
                    thresholds_dto.temperature_celsius_max,
                ),
            ),
        )
        # await self.uow.add(recommendation)
        # await self.uow.commit()
        return GenerateRecommendationResponse(
            patient_history=patient_history,
            recommendation=RecommendationDTO(
                id=recommendation.id,
                patient_id=patient_id,
                thresholds=thresholds_dto,
            ),
        )
