from dataclasses import dataclass
from typing import NewType
from uuid import UUID

PatientId = NewType('PatientId', UUID)


@dataclass(frozen=True, slots=True)
class Patient:
    id: PatientId
