from dataclasses import dataclass, field

from health_backend.application.common.errors import EmailAlreadyInUse
from health_backend.domain.doctor.entity import Doctor, DoctorId
from health_backend.domain.doctor.repository import DoctorRepository


@dataclass(frozen=True, slots=True)
class InMemoryDoctorRepository(DoctorRepository):
    doctors: dict[DoctorId, Doctor] = field(default_factory=dict)

    async def add(self, doctor: Doctor) -> None:
        if any(d.email == doctor.email for d in self.doctors.values()):
            raise EmailAlreadyInUse
        self.doctors[doctor.id] = doctor

    async def get_by_id(self, doctor_id: DoctorId) -> Doctor | None:
        return self.doctors.get(doctor_id)
