from abc import abstractmethod
from typing import Protocol

from health_backend.domain.doctor.entity import Doctor


class DoctorRepository(Protocol):
    @abstractmethod
    async def add(self, doctor: Doctor) -> None: ...
