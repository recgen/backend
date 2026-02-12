from dataclasses import dataclass

from health_backend.domain.common.vo import Range


@dataclass(frozen=True, slots=True)
class Thresholds:
    systolic_blood_pressure: Range
    diastolic_blood_pressure: Range
    temperature_celsius: Range
