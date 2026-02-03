from dataclasses import dataclass
from decimal import Decimal
from typing import Self
from uuid import UUID

from health_backend.domain.recommendation.vo import Thresholds


@dataclass(frozen=True, slots=True)
class ThresholdsDTO:
    systolic_blood_pressure_min: Decimal
    systolic_blood_pressure_max: Decimal
    diastolic_blood_pressure_min: Decimal
    diastolic_blood_pressure_max: Decimal
    temperature_celsius_min: Decimal
    temperature_celsius_max: Decimal

    @classmethod
    def from_entity(cls, thresholds: Thresholds) -> Self:
        return cls(
            systolic_blood_pressure_min=thresholds.systolic_blood_pressure.minimum,
            systolic_blood_pressure_max=thresholds.systolic_blood_pressure.maximum,
            diastolic_blood_pressure_min=thresholds.diastolic_blood_pressure.minimum,
            diastolic_blood_pressure_max=thresholds.diastolic_blood_pressure.maximum,
            temperature_celsius_min=thresholds.temperature_celsius.minimum,
            temperature_celsius_max=thresholds.temperature_celsius.maximum,
        )


@dataclass(frozen=True, slots=True)
class RecommendationDTO:
    id: UUID
    patient_id: UUID
    thresholds: ThresholdsDTO


@dataclass(frozen=True, slots=True)
class GenerateRecommendationResponse:
    patient_history: str
    recommendation: RecommendationDTO
