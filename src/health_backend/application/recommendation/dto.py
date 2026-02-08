from dataclasses import dataclass
from decimal import Decimal
from typing import Self
from uuid import UUID

from health_backend.domain.recommendation.entity import Recommendation
from health_backend.domain.recommendation.vo import Thresholds


@dataclass(frozen=True, slots=True)
class ThresholdsDTO:
    systolic_blood_pressure_min: int
    systolic_blood_pressure_max: int
    diastolic_blood_pressure_min: int
    diastolic_blood_pressure_max: int
    temperature_celsius_min: int | float
    temperature_celsius_max: int | float

    @classmethod
    def from_vo(cls, thresholds: Thresholds) -> Self:
        return cls(
            systolic_blood_pressure_min=int(thresholds.systolic_blood_pressure.minimum),
            systolic_blood_pressure_max=int(thresholds.systolic_blood_pressure.maximum),
            diastolic_blood_pressure_min=int(thresholds.diastolic_blood_pressure.minimum),
            diastolic_blood_pressure_max=int(thresholds.diastolic_blood_pressure.maximum),
            temperature_celsius_min=float(thresholds.temperature_celsius.minimum),
            temperature_celsius_max=float(thresholds.temperature_celsius.maximum),
        )


@dataclass(frozen=True, slots=True)
class RecommendationDTO:
    id: UUID
    patient_id: UUID
    patient_history: str
    thresholds: ThresholdsDTO

    @classmethod
    def from_entity(cls, recommendation: Recommendation) -> Self:
        return cls(
            id=recommendation.id,
            patient_id=recommendation.patient_id,
            patient_history=recommendation.patient_history.value,
            thresholds=ThresholdsDTO.from_vo(recommendation.thresholds),
        )


@dataclass(frozen=True, slots=True)
class GenerateRecommendationForPatientResponse:
    recommendation: RecommendationDTO


@dataclass(frozen=True, slots=True)
class PaginatedRecommendationsResponse:
    recommendations: list[RecommendationDTO]
    page: int
    size: int
    total: int
