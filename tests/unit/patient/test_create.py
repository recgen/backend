from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from health_backend.application.patient.create import CreatePatient
from health_backend.application.patient.dto import CreatePatientRequest
from health_backend.domain.common.errors import EmptyNameError
from health_backend.domain.common.vo import FutureDateError, Gender
from health_backend.domain.doctor.entity import DoctorId
from health_backend.domain.patient.repository import PatientRepository
from tests.unit.stubs.idp import StubIdp


@pytest.mark.asyncio
async def test_creating_patient_with_empty_name_fails(
    create_patient_interactor: CreatePatient,
    idp: StubIdp,
) -> None:
    request = CreatePatientRequest(
        name='',
        gender=Gender.MALE,
        birth_date=datetime.now(tz=UTC),
    )
    idp.set_doctor_id(DoctorId(uuid4()))

    with pytest.raises(EmptyNameError):
        await create_patient_interactor.execute(request)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'offset',
    [
        timedelta(seconds=5),
        timedelta(minutes=3),
        timedelta(hours=17),
    ],
)
async def test_creating_patient_with_future_birth_date_fails(
    offset: timedelta,
    create_patient_interactor: CreatePatient,
    idp: StubIdp,
) -> None:
    request = CreatePatientRequest(
        name='John Doe',
        gender=Gender.MALE,
        birth_date=datetime.now(tz=UTC) + offset,
    )
    idp.set_doctor_id(DoctorId(uuid4()))

    with pytest.raises(FutureDateError):
        await create_patient_interactor.execute(request)


@pytest.mark.asyncio
async def test_creating_patient_with_valid_data_succeeds(
    create_patient_interactor: CreatePatient,
    idp: StubIdp,
    patient_repository: PatientRepository,
) -> None:
    request = CreatePatientRequest(
        name='John Doe',
        gender=Gender.MALE,
        birth_date=datetime.now(tz=UTC),
    )
    idp.set_doctor_id(DoctorId(uuid4()))

    response = await create_patient_interactor.execute(request)

    patient_id = response.id
    assert (await patient_repository.get_by_id(patient_id)) is not None
