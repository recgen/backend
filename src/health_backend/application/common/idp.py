from abc import abstractmethod
from typing import Protocol

from health_backend.domain.doctor.entity import DoctorId


class DoctorIdProvider(Protocol):
    @abstractmethod
    def get_id(self) -> DoctorId | None: ...
