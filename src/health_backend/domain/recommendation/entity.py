from dataclasses import dataclass
from typing import NewType, Self
from uuid import UUID, uuid4

from health_backend.domain.patient.entity import PatientId
from health_backend.domain.patient.vo import PatientHistory
from health_backend.domain.recommendation.vo import Thresholds

RecommendationId = NewType('RecommendationId', UUID)


@dataclass
class Recommendation:
    id: RecommendationId
    patient_id: PatientId
    patient_history: PatientHistory
    thresholds: Thresholds

    @classmethod
    def create(
        cls,
        patient_id: PatientId,
        patient_history: PatientHistory,
        thresholds: Thresholds,
    ) -> Self:
        return cls(
            id=RecommendationId(uuid4()),
            patient_id=patient_id,
            patient_history=patient_history,
            thresholds=thresholds,
        )
