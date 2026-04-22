from abc import abstractmethod
from typing import Protocol

from health_backend.domain.common.vo import Name
from health_backend.domain.patient.entity import Patient, PatientId


class PatientRepository(Protocol):
    @abstractmethod
    async def add(self, patient: Patient) -> None: ...

    @abstractmethod
    async def update(self, patient: Patient) -> None: ...

    @abstractmethod
    async def get_by_id(self, id: PatientId) -> Patient | None: ...

    @abstractmethod
    async def get_active_paginated(
        self,
        name_like: Name | None,
        page: int,
        size: int,
    ) -> tuple[list[Patient], int]: ...
