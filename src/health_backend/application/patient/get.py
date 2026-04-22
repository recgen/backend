from dataclasses import dataclass

from health_backend.application.common.errors import NotFoundError
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.application.patient.dto import PaginatedPatientsResponse, PatientDTO
from health_backend.domain.common.vo import Name
from health_backend.domain.patient.entity import PatientId
from health_backend.domain.patient.repository import PatientRepository


@dataclass(frozen=True, slots=True)
class GetPatient:
    idp: DoctorIdProvider
    repo: PatientRepository

    async def execute(self, id: PatientId) -> PatientDTO:
        self.idp.require_auth()

        patient = await self.repo.get_by_id(id)
        if patient is None:
            raise NotFoundError

        return PatientDTO.from_entity(patient)


@dataclass(frozen=True, slots=True)
class GetPaginatedPatients:
    idp: DoctorIdProvider
    repo: PatientRepository

    async def execute(
        self,
        name_like: str | None,
        page: int,
        size: int,
    ) -> PaginatedPatientsResponse:
        self.idp.require_auth()

        patients, total = await self.repo.get_active_paginated(
            Name(name_like) if name_like is not None else None,
            page,
            size,
        )

        return PaginatedPatientsResponse(
            patients=[PatientDTO.from_entity(p) for p in patients],
            page=page,
            size=size,
            total=total,
        )
