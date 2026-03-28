import pytest

from health_backend.application.common.committer import Committer
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.application.patient.create import CreatePatient
from health_backend.domain.patient.repository import PatientRepository
from tests.unit.fakes.persistence import InMemoryPatientRepository


@pytest.fixture
def create_patient_interactor(
    idp: DoctorIdProvider, patient_repository: PatientRepository, committer: Committer
) -> CreatePatient:
    return CreatePatient(idp=idp, patient_repo=patient_repository, committer=committer)


@pytest.fixture
def patient_repository() -> InMemoryPatientRepository:
    return InMemoryPatientRepository()
