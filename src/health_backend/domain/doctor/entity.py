from ast import Name
from dataclasses import dataclass
from typing import NewType
from uuid import UUID

from health_backend.domain.common.vo import Email

DoctorId = NewType('DoctorId', UUID)


@dataclass(frozen=True, slots=True)
class Doctor:
    id: DoctorId
    name: Name
    email: Email
    hashed_password: str
