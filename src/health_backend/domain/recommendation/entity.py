from dataclasses import dataclass
from typing import NewType, Self
from uuid import UUID, uuid4

from health_backend.domain.patient.entity import PatientId
from health_backend.domain.recommendation.vo import Thresholds

RecommendationId = NewType('RecommendationId', UUID)


@dataclass(frozen=True, slots=True)
class Recommendation:
    id: RecommendationId
    patient_id: PatientId
    thresholds: Thresholds

    @classmethod
    def create(
        cls,
        patient_id: PatientId,
        thresholds: Thresholds,
    ) -> Self:
        return cls(
            id=RecommendationId(uuid4()),
            patient_id=patient_id,
            thresholds=thresholds,
        )
