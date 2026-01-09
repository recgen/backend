from health_backend.domain.doctor.entity import Doctor
from health_backend.domain.doctor.repository import DoctorRepository


class InMemoryDoctorRepository(DoctorRepository):
    def __init__(self) -> None:
        self._data: list[Doctor] = []

    async def get_by_user_id(self, user_id: int) -> Doctor | None:
        selected = [doctor for doctor in self._data if doctor.user_id == user_id]
        if not selected:
            return None
        return selected[0]

    async def add(self, doctor: Doctor) -> None:
        self._data.append(doctor)
