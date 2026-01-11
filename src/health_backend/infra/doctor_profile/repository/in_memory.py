from health_backend.domain.doctor_profile.entity import DoctorProfile
from health_backend.domain.doctor_profile.repository import DoctorProfileRepository
from health_backend.domain.user.entity import UserId


class InMemoryDoctorProfileRepository(DoctorProfileRepository):
    def __init__(self) -> None:
        self._data: list[DoctorProfile] = []

    async def add(self, doctor_profile: DoctorProfile) -> None:
        self._data.append(doctor_profile)

    async def get_by_user_id(self, user_id: UserId) -> DoctorProfile | None:
        selected = [doctor for doctor in self._data if doctor.user_id == user_id]
        if not selected:
            return None
        return selected[0]
