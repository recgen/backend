from abc import abstractmethod
from typing import Protocol

from health_backend.domain.patient.entity import Patient, PatientId


class PatientRepository(Protocol):
    @abstractmethod
    async def get_by_id(self, id: PatientId) -> Patient | None: ...

    @abstractmethod
    async def get_paginated(self, page: int, size: int) -> tuple[list[Patient], int]: ...
