from dataclasses import dataclass
from decimal import Decimal
from typing import Self
from uuid import UUID

from health_backend.domain.recommendation.vo import Thresholds


@dataclass(frozen=True, slots=True)
class ThresholdsDTO:
    systolic_blood_pressure_min: int
    systolic_blood_pressure_max: int
    diastolic_blood_pressure_min: int
    diastolic_blood_pressure_max: int
    temperature_celsius_min: int | float
    temperature_celsius_max: int | float


@dataclass(frozen=True, slots=True)
class RecommendationDTO:
    id: UUID
    patient_id: UUID
    thresholds: ThresholdsDTO


@dataclass(frozen=True, slots=True)
class GenerateRecommendationResponse:
    patient_history: str
    recommendation: RecommendationDTO
