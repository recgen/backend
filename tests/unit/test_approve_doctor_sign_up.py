from uuid import uuid4

import pytest

from health_backend.application.admin.approve_doctor_sign_up import ApproveDoctorSignUp
from health_backend.application.common import identity_provider
from health_backend.application.common.errors import (
    ForbiddenActionError,
    UnauthorizedError,
    UserDoesNotExist,
    UserIsNotDoctor,
    WrongUserStatus,
)
from health_backend.domain.user.entity import User, UserId, UserRole, UserStatus
from health_backend.infra.common.identity_provider.mock import MockIdentityProvider
from health_backend.infra.user.repository.in_memory import InMemoryUserRepository


def user_factory() -> User:
    return User.new(
        first_name='John',
        last_name='Doe',
        email='johndoe@examle.com',
        password_hash='xxxyyyzzz',
        status=UserStatus.ACTIVE,
        roles=[],
    )


@pytest.fixture
def doctor_user() -> User:
    user = user_factory()
    user.add_role(UserRole.DOCTOR)
    return user


@pytest.fixture
def admin_user() -> User:
    user = user_factory()
    user.add_role(UserRole.ADMIN)
    return user


@pytest.mark.asyncio
async def test_valid(
    doctor_user: User,
    admin_user: User,
) -> None:
    user_repo = InMemoryUserRepository()
    doctor_user.set_status(UserStatus.ACTIVATION_PENDING)
    await user_repo.add(doctor_user)

    identity_provider = MockIdentityProvider(admin_user)

    use_case = ApproveDoctorSignUp(
        user_repo=user_repo,
        identity_provider=identity_provider,
    )

    await use_case.execute(doctor_user_id=doctor_user.id)

    user = await user_repo.get_by_id(doctor_user.id)
    assert user is not None
    assert user.is_active


@pytest.mark.asyncio
async def test_no_current_user(doctor_user: User) -> None:
    user_repo = InMemoryUserRepository()
    doctor_user.set_status(UserStatus.ACTIVATION_PENDING)
    await user_repo.add(doctor_user)

    identity_provider = MockIdentityProvider(None)

    use_case = ApproveDoctorSignUp(
        user_repo=user_repo,
        identity_provider=identity_provider,
    )

    with pytest.raises(UnauthorizedError):
        await use_case.execute(doctor_user_id=doctor_user.id)


@pytest.mark.asyncio
async def test_admin_inactive(doctor_user: User, admin_user: User) -> None:
    user_repo = InMemoryUserRepository()
    doctor_user.set_status(UserStatus.ACTIVATION_PENDING)
    await user_repo.add(doctor_user)

    admin_user.set_status(UserStatus.INACTIVE)
    identity_provider = MockIdentityProvider(admin_user)

    use_case = ApproveDoctorSignUp(
        user_repo=user_repo,
        identity_provider=identity_provider,
    )

    with pytest.raises(ForbiddenActionError):
        await use_case.execute(doctor_user_id=doctor_user.id)


@pytest.mark.asyncio
async def test_non_admin(doctor_user: User, admin_user: User) -> None:
    user_repo = InMemoryUserRepository()
    doctor_user.set_status(UserStatus.ACTIVATION_PENDING)
    await user_repo.add(doctor_user)

    user = admin_user
    user.remove_role(UserRole.ADMIN)

    identity_provider = MockIdentityProvider(user)

    use_case = ApproveDoctorSignUp(
        user_repo=user_repo,
        identity_provider=identity_provider,
    )

    with pytest.raises(ForbiddenActionError):
        await use_case.execute(doctor_user_id=doctor_user.id)


@pytest.mark.asyncio
async def test_user_does_not_exist(admin_user: User) -> None:
    user_repo = InMemoryUserRepository()
    identity_provider = MockIdentityProvider(admin_user)

    use_case = ApproveDoctorSignUp(
        user_repo=user_repo,
        identity_provider=identity_provider,
    )

    with pytest.raises(UserDoesNotExist):
        await use_case.execute(doctor_user_id=UserId(uuid4()))


@pytest.mark.asyncio
async def test_user_is_not_doctor(admin_user: User) -> None:
    user_repo = InMemoryUserRepository()
    await user_repo.add(admin_user)

    identity_provider = MockIdentityProvider(admin_user)

    use_case = ApproveDoctorSignUp(
        user_repo=user_repo,
        identity_provider=identity_provider,
    )

    with pytest.raises(UserIsNotDoctor):
        await use_case.execute(doctor_user_id=admin_user.id)


@pytest.mark.asyncio
async def test_doctor_is_already_active(doctor_user: User, admin_user: User) -> None:
    user_repo = InMemoryUserRepository()
    doctor_user.set_status(UserStatus.ACTIVE)
    await user_repo.add(doctor_user)

    identity_provider = MockIdentityProvider(admin_user)

    use_case = ApproveDoctorSignUp(
        user_repo=user_repo,
        identity_provider=identity_provider,
    )

    with pytest.raises(WrongUserStatus):
        await use_case.execute(doctor_user_id=doctor_user.id)
