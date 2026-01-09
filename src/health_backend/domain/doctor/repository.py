from abc import ABC, abstractmethod

from health_backend.domain.doctor.entity import Doctor


class DoctorRepository(ABC):
    @abstractmethod
    async def add(self, doctor: Doctor) -> None: ...
