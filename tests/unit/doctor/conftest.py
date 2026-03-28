import pytest

from health_backend.application.common.access_token_generator import AccessTokenGenerator
from health_backend.application.common.committer import Committer
from health_backend.application.common.password_hasher import PasswordHasher
from health_backend.application.doctor.signup import DoctorSignup
from health_backend.domain.doctor.repository import DoctorRepository
from tests.unit.fakes.auth import FakeAccessTokenGenerator, FakePasswordHasher
from tests.unit.fakes.persistence import InMemoryDoctorRepository


@pytest.fixture
def doctor_repository() -> InMemoryDoctorRepository:
    return InMemoryDoctorRepository()


@pytest.fixture
def password_hasher() -> FakePasswordHasher:
    return FakePasswordHasher()


@pytest.fixture
def access_token_generator() -> FakeAccessTokenGenerator:
    return FakeAccessTokenGenerator()


@pytest.fixture
def signup_interactor(
    doctor_repository: DoctorRepository,
    committer: Committer,
    password_hasher: PasswordHasher,
    access_token_generator: AccessTokenGenerator,
) -> DoctorSignup:
    return DoctorSignup(
        repo=doctor_repository,
        committer=committer,
        password_hasher=password_hasher,
        access_token_generator=access_token_generator,
    )
