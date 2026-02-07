from health_backend.application.common.errors import EmailAlreadyInUse
from health_backend.domain.doctor.entity import Doctor
from health_backend.domain.doctor.repository import DoctorRepository


class InMemoryDoctorRepository(DoctorRepository):
    doctors = {}

    async def add(self, doctor: Doctor) -> None:
        if any(d.email == doctor.email for d in self.doctors.values()):
            raise EmailAlreadyInUse
        self.doctors[doctor.id] = doctor
