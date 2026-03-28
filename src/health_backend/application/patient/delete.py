from dataclasses import dataclass

from health_backend.application.common.errors import NotFoundError, UnauthorizedError
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.application.common.uow import UnitOfWork
from health_backend.domain.common.errors import InactiveError
from health_backend.domain.patient.entity import PatientId
from health_backend.domain.patient.repository import PatientRepository


@dataclass(frozen=True, slots=True)
class DeletePatient:
    idp: DoctorIdProvider
    uow: UnitOfWork
    repo: PatientRepository

    async def execute(self, id: PatientId) -> None:
        doctor_id = self.idp.get_id()
        if doctor_id is None:
            raise UnauthorizedError
        patient = await self.repo.get_by_id(id)
        if patient is None:
            raise NotFoundError
        if patient.is_active is False:
            raise InactiveError
        patient.is_active = False
        self.uow.add(patient)
        await self.uow.commit()
