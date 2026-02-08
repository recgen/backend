from dataclasses import dataclass

from attr import frozen

from health_backend.domain.common.vo import Range


@frozen
class Thresholds:
    systolic_blood_pressure: Range
    diastolic_blood_pressure: Range
    temperature_celsius: Range
