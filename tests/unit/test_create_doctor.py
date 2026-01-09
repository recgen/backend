from uuid import uuid4

import pytest

from health_backend.application.admin.create_doctor import CreateDoctor
from health_backend.application.admin.dto import CreateDoctorInput, CreateDoctorOutput
from health_backend.application.common import identity_provider
from health_backend.application.common.exceptions import UnauthorizedError
from health_backend.domain.admin.entity import Admin
from health_backend.domain.user.entity import User
from health_backend.infra.admin.repository.in_memory import InMemoryAdminRepository
from health_backend.infra.common.identity_provider.mock import MockIdentityProvider
from health_backend.infra.doctor.repository.in_memory import InMemoryDoctorRepository
from health_backend.infra.user.repository.in_memory import InMemoryUserRepository


@pytest.fixture
def repos():
    return {
        'admin': InMemoryAdminRepository(),
        'doctor': InMemoryDoctorRepository(),
        'user': InMemoryUserRepository(),
    }


@pytest.fixture
def doctor() -> CreateDoctorInput:
    return CreateDoctorInput(
        first_name='Jane',
        last_name='Doe',
        email='notfake@notfake.com',
        password_hash='',
        department_id=uuid4(),
    )


@pytest.fixture
def user() -> User:
    return User(
        id=uuid4(),
        first_name='John',
        last_name='Doe',
        email='fake@fake.com',
        password_hash='cute_hash',
    )


@pytest.mark.asyncio
async def test_create_doctor_as_admin(repos, user, doctor) -> None:
    admin = Admin(
        user_id=user.id,
    )

    await repos['user'].add(user)
    await repos['admin'].add(admin)

    identity_provider = MockIdentityProvider(user)

    use_case = CreateDoctor(
        identity_provider=identity_provider,
        admin_repo=repos['admin'],
        user_repo=repos['user'],
        doctor_repo=repos['doctor'],
    )
    result = await use_case.execute(doctor)

    assert result.first_name == doctor.first_name
    assert result.last_name == doctor.last_name
    assert result.email == doctor.email
    assert result.department_id == doctor.department_id


@pytest.mark.asyncio
async def test_create_doctor_as_regular_user(repos, user, doctor) -> None:
    await repos['user'].add(user)

    identity_provider = MockIdentityProvider(user)

    use_case = CreateDoctor(
        identity_provider=identity_provider,
        admin_repo=repos['admin'],
        user_repo=repos['user'],
        doctor_repo=repos['doctor'],
    )

    with pytest.raises(UnauthorizedError):
        await use_case.execute(doctor)
