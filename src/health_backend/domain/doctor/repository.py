from abc import abstractmethod
from typing import Protocol

from health_backend.domain.common.vo import Email
from health_backend.domain.doctor.entity import Doctor, DoctorId


class DoctorRepository(Protocol):
    @abstractmethod
    async def add(self, doctor: Doctor) -> None: ...

    @abstractmethod
    async def get_by_id(self, doctor_id: DoctorId) -> Doctor | None: ...

    @abstractmethod
    async def get_by_email(self, email: Email) -> Doctor | None: ...
