from dataclasses import dataclass

from health_backend.application.common.errors import NotFound, Unauthorized
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.application.doctor.dto import DoctorDTO
from health_backend.domain.doctor.repository import DoctorRepository


@dataclass(frozen=True, slots=True)
class GetMe:
    idp: DoctorIdProvider
    repo: DoctorRepository

    async def execute(self) -> DoctorDTO:
        doctor_id = self.idp.get_id()
        if doctor_id is None:
            raise Unauthorized
        doctor = await self.repo.get_by_id(doctor_id)
        if doctor is None:
            raise NotFound
        return DoctorDTO.from_entity(doctor)
