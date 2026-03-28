from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from health_backend.domain.doctor.entity import DoctorId


@dataclass(frozen=True, slots=True)
class AccessToken:
    value: str
    doctor_id: DoctorId


class AccessTokenGenerator(Protocol):
    @abstractmethod
    def generate(self, doctor_id: DoctorId, expire_in: int) -> AccessToken: ...
