from health_backend.application.common.errors import EmailAlreadyInUseError
from health_backend.domain.common.vo import Email
from health_backend.domain.doctor.entity import Doctor, DoctorId
from health_backend.domain.doctor.repository import DoctorRepository


class InMemoryDoctorRepository(DoctorRepository):
    def __init__(self) -> None:
        self.doctors: dict[DoctorId, Doctor] = {}

    async def add(self, doctor: Doctor) -> None:
        if any(d.email == doctor.email for d in self.doctors.values()):
            raise EmailAlreadyInUseError
        self.doctors[doctor.id] = doctor

    async def get_by_id(self, doctor_id: DoctorId) -> Doctor | None:
        return self.doctors.get(doctor_id)

    async def get_by_email(self, email: Email) -> Doctor | None:
        for d in self.doctors.values():
            if d.email == email:
                return d
        return None
