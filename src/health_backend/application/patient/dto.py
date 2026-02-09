from dataclasses import dataclass
from datetime import datetime
from typing import Self
from uuid import UUID

from health_backend.domain.common.vo import Gender
from health_backend.domain.patient.entity import Patient


@dataclass(frozen=True, slots=True)
class CreatePatientRequest:
    name: str
    gender: Gender
    birth_date: datetime


@dataclass(frozen=True, slots=True)
class CreatePatientResponse:
    id: UUID
    name: str
    gender: Gender
    birth_date: datetime

    @classmethod
    def from_entity(cls, patient: Patient) -> Self:
        return cls(
            id=patient.id,
            name=patient.name.value,
            gender=patient.gender,
            birth_date=patient.birth_date,
        )


@dataclass(frozen=True, slots=True)
class PatientDTO:
    id: UUID
    name: str
    gender: Gender
    birth_date: datetime

    @classmethod
    def from_entity(cls, patient: Patient) -> Self:
        return cls(
            id=patient.id,
            name=patient.name.value,
            gender=patient.gender,
            birth_date=patient.birth_date,
        )


@dataclass(frozen=True, slots=True)
class PaginatedPatientsResponse:
    patients: list[PatientDTO]
    page: int
    size: int
    total: int
