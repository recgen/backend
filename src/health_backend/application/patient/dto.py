from dataclasses import dataclass
from typing import Self
from uuid import UUID

from health_backend.domain.patient.entity import Patient


@dataclass(frozen=True, slots=True)
class CreatePatientRequest:
    name: str


@dataclass(frozen=True, slots=True)
class CreatePatientResponse:
    id: UUID
    name: str

    @classmethod
    def from_entity(cls, patient: Patient) -> Self:
        return cls(
            id=patient.id,
            name=patient.name.value,
        )


@dataclass(frozen=True, slots=True)
class PatientDTO:
    id: UUID
    name: str

    @classmethod
    def from_entity(cls, patient: Patient) -> Self:
        return cls(
            id=patient.id,
            name=patient.name.value,
        )


@dataclass(frozen=True, slots=True)
class PaginatedPatientsResponse:
    patients: list[PatientDTO]
    page: int
    size: int
    total: int
