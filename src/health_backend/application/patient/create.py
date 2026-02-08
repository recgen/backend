from dataclasses import dataclass

from health_backend.application.common.errors import Unauthorized
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.application.common.uow import UnitOfWork
from health_backend.application.patient.dto import CreatePatientRequest, CreatePatientResponse
from health_backend.domain.patient.entity import Patient


@dataclass(frozen=True, slots=True)
class CreatePatient:
    idp: DoctorIdProvider
    uow: UnitOfWork

    async def execute(self, request: CreatePatientRequest) -> CreatePatientResponse:
        doctor_id = self.idp.get_id()
        if doctor_id is None:
            raise Unauthorized
        patient = Patient.create(
            name=request.name,
        )
        self.uow.add(patient)
        await self.uow.commit()
        return CreatePatientResponse.from_entity(patient)
