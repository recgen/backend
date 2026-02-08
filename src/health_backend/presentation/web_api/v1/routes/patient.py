from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from health_backend.application.patient.create import CreatePatient
from health_backend.application.patient.dto import (
    CreatePatientRequest,
    CreatePatientResponse,
    PaginatedPatientsResponse,
    PatientDTO,
)
from health_backend.application.patient.get import GetPaginatedPatients, GetPatient
from health_backend.domain.patient.entity import PatientId

router = APIRouter(
    tags=['Patient'],
    prefix='/patient',
    route_class=DishkaRoute,
)


@router.post('/')
async def create_patient(
    request: CreatePatientRequest, use_case: FromDishka[CreatePatient]
) -> CreatePatientResponse:
    return await use_case.execute(request)


@router.get('/')
async def create_patient(
    use_case: FromDishka[GetPaginatedPatients],
    page: int = 1,
    size: int = 20,
) -> PaginatedPatientsResponse:
    return await use_case.execute(page, size)
