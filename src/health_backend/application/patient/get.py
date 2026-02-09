from dataclasses import dataclass

from health_backend.application.common.errors import NotFound, Unauthorized
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.application.patient.dto import PaginatedPatientsResponse, PatientDTO
from health_backend.domain.patient.entity import PatientId
from health_backend.domain.patient.repository import PatientRepository


@dataclass(frozen=True, slots=True)
class GetPatient:
    idp: DoctorIdProvider
    repo: PatientRepository

    async def execute(self, id: PatientId) -> PatientDTO:
        doctor_id = self.idp.get_id()
        if doctor_id is None:
            raise Unauthorized
        patient = await self.repo.get_by_id(id)
        if patient is None:
            raise NotFound
        return PatientDTO.from_entity(patient)


@dataclass(frozen=True, slots=True)
class GetPaginatedPatients:
    idp: DoctorIdProvider
    repo: PatientRepository

    async def execute(self, page: int, size: int) -> PaginatedPatientsResponse:
        doctor_id = self.idp.get_id()
        if doctor_id is None:
            raise Unauthorized
        patients, total = await self.repo.get_active_paginated(page, size)
        return PaginatedPatientsResponse(
            patients=[PatientDTO.from_entity(p) for p in patients],
            page=page,
            size=size,
            total=total,
        )
