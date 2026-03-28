from dataclasses import dataclass

from health_backend.application.common.committer import Committer
from health_backend.application.common.errors import UnauthorizedError
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.application.patient.dto import CreatePatientRequest, CreatePatientResponse
from health_backend.domain.patient.entity import Patient
from health_backend.domain.patient.repository import PatientRepository


@dataclass(frozen=True, slots=True)
class CreatePatient:
    idp: DoctorIdProvider
    patient_repo: PatientRepository
    committer: Committer

    async def execute(self, request: CreatePatientRequest) -> CreatePatientResponse:
        doctor_id = self.idp.get_id()
        if doctor_id is None:
            raise UnauthorizedError

        patient = Patient.create(
            name=request.name,
            birth_date=request.birth_date,
            gender=request.gender,
        )
        await self.patient_repo.add(patient)
        await self.committer.commit()

        return CreatePatientResponse.from_entity(patient)
