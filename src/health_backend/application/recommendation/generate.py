from dataclasses import dataclass

from health_backend.application.common.committer import Committer
from health_backend.application.common.errors import NotFoundError, UnauthorizedError
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.application.recommendation.dto import (
    GenerateRecommendationForPatientResponse,
    RecommendationDTO,
)
from health_backend.application.recommendation.generator import ThresholdsGenerator
from health_backend.domain.common.errors import InactiveError
from health_backend.domain.common.vo import Range
from health_backend.domain.patient.entity import PatientId
from health_backend.domain.patient.repository import PatientRepository
from health_backend.domain.patient.vo import PatientHistory
from health_backend.domain.recommendation.entity import Recommendation
from health_backend.domain.recommendation.repository import RecommendationRepository
from health_backend.domain.recommendation.vo import Thresholds


@dataclass(frozen=True, slots=True)
class GenerateRecommendationForPatient:
    generator: ThresholdsGenerator
    patient_repo: PatientRepository
    recommendation_repo: RecommendationRepository
    idp: DoctorIdProvider
    committer: Committer

    async def execute(
        self, patient_id: PatientId, patient_history: str
    ) -> GenerateRecommendationForPatientResponse:
        doctor_id = self.idp.get_id()
        if doctor_id is None:
            raise UnauthorizedError

        patient_history_vo = PatientHistory(patient_history)
        patient = await self.patient_repo.get_by_id(patient_id)

        if patient is None:
            raise NotFoundError
        if patient.is_active is False:
            raise InactiveError

        thresholds_dto = await self.generator.generate(patient_history)

        recommendation = Recommendation.create(
            patient_id,
            patient_history_vo,
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

        await self.recommendation_repo.add(recommendation)
        await self.committer.commit()

        return GenerateRecommendationForPatientResponse(
            recommendation=RecommendationDTO(
                id=recommendation.id,
                patient_id=patient_id,
                patient_history=patient_history,
                thresholds=thresholds_dto,
            ),
        )
