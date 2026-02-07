from dataclasses import dataclass
from typing import Self
from uuid import UUID

from health_backend.domain.doctor.entity import Doctor


@dataclass(frozen=True, slots=True)
class DoctorSignupRequest:
    name: str
    email: str
    password: str


@dataclass(frozen=True, slots=True)
class DoctorDTO:
    id: UUID
    name: str
    email: str

    @classmethod
    def from_entity(cls, doctor: Doctor) -> Self:
        return cls(
            id=doctor.id,
            name=doctor.name.value,
            email=doctor.email.value,
        )


@dataclass(frozen=True, slots=True)
class DoctorAuthResponse:
    access_token: str
    doctor: DoctorDTO
