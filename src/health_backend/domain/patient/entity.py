from dataclasses import dataclass
from typing import NewType, Self
from uuid import UUID, uuid4

from health_backend.domain.common.vo import Name

PatientId = NewType('PatientId', UUID)


@dataclass
class Patient:
    id: PatientId
    name: Name

    @classmethod
    def create(
        cls,
        name: str,
    ) -> Self:
        return cls(
            id=PatientId(uuid4()),
            name=Name(name),
        )
