from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from health_backend.application.patient.create import CreatePatient
from health_backend.application.patient.delete import DeletePatient
from health_backend.application.patient.dto import (
    CreatePatientRequest,
    CreatePatientResponse,
    PaginatedPatientsResponse,
)
from health_backend.application.patient.get import GetPaginatedPatients
from health_backend.domain.patient.entity import PatientId

router = APIRouter(
    tags=['Patient'],
    prefix='/patients',
    route_class=DishkaRoute,
)


@router.post('', status_code=201)
async def create_patient(
    request: CreatePatientRequest, use_case: FromDishka[CreatePatient]
) -> CreatePatientResponse:
    return await use_case.execute(request)


@router.get('')
async def get_paginated(
    use_case: FromDishka[GetPaginatedPatients],
    page: int = 1,
    size: int = 20,
) -> PaginatedPatientsResponse:
    return await use_case.execute(page, size)


@router.delete('/{id}', status_code=204)
async def delete(
    use_case: FromDishka[DeletePatient],
    id: PatientId,
) -> None:
    await use_case.execute(id)
