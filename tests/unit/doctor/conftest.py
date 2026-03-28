import pytest

from health_backend.application.common.access_token_generator import AccessTokenGenerator
from health_backend.application.common.password_hasher import PasswordHasher
from health_backend.application.doctor.signup import DoctorSignup
from health_backend.domain.doctor.repository import DoctorRepository
from tests.unit.fakes.auth import FakeAccessTokenGenerator, FakePasswordHasher
from tests.unit.fakes.persistence import InMemoryDoctorRepository


@pytest.fixture
def doctor_repository() -> DoctorRepository:
    return InMemoryDoctorRepository()


@pytest.fixture
def password_hasher() -> PasswordHasher:
    return FakePasswordHasher()


@pytest.fixture
def access_token_generator() -> AccessTokenGenerator:
    return FakeAccessTokenGenerator()


@pytest.fixture
def signup_interactor(
    doctor_repository: DoctorRepository,
    password_hasher: PasswordHasher,
    access_token_generator: AccessTokenGenerator,
) -> DoctorSignup:
    return DoctorSignup(
        repo=doctor_repository,
        password_hasher=password_hasher,
        access_token_generator=access_token_generator,
    )
