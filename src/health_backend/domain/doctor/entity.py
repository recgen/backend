from dataclasses import dataclass
from typing import NewType, Self
from uuid import UUID, uuid4

from health_backend.domain.common.vo import Email, Name

DoctorId = NewType('DoctorId', UUID)


@dataclass(frozen=True, slots=True)
class Doctor:
    id: DoctorId
    name: Name
    email: Email
    hashed_password: str

    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        hashed_password: str,
    ) -> Self:
        return cls(
            id=DoctorId(uuid4()),
            name=Name(name),
            email=Email(email),
            hashed_password=hashed_password,
        )
