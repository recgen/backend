from dataclasses import dataclass
from typing import Self

from health_backend.domain.doctor.entity import Doctor, DoctorId


@dataclass(frozen=True, slots=True)
class DoctorSignupRequest:
    name: str
    email: str
    password: str


@dataclass(frozen=True, slots=True)
class DoctorDTO:
    id: DoctorId
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


@dataclass(frozen=True, slots=True)
class DoctorLoginRequest:
    email: str
    password: str
