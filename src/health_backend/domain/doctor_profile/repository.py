from abc import ABC, abstractmethod

from health_backend.domain.doctor_profile.entity import DoctorProfile
from health_backend.domain.user.entity import UserId


class DoctorProfileRepository(ABC):
    @abstractmethod
    async def add(self, doctor_profile: DoctorProfile) -> None: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UserId) -> DoctorProfile | None: ...
