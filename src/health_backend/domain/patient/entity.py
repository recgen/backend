from dataclasses import dataclass
from datetime import datetime
from typing import NewType, Self
from uuid import UUID, uuid4

from health_backend.domain.common.vo import Gender, Name

PatientId = NewType('PatientId', UUID)


@dataclass
class Patient:
    id: PatientId
    name: Name
    birth_date: datetime
    gender: Gender
    is_active: bool

    @classmethod
    def create(
        cls,
        name: str,
        birth_date: datetime,
        gender: str | Gender,
    ) -> Self:
        return cls(
            id=PatientId(uuid4()),
            name=Name(name),
            birth_date=birth_date,
            gender=Gender(gender),
            is_active=True,
        )
