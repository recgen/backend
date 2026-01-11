import pytest

from health_backend.application.admin.approve_doctor_sign_up import ApproveDoctorSignUp
from health_backend.application.doctor.dto import SignUpDoctorProfileInput
from health_backend.application.doctor.sign_up import DoctorSignUp
from health_backend.domain.user.entity import User, UserRole, UserStatus
from health_backend.infra.common.identity_provider.mock import MockIdentityProvider
from health_backend.infra.common.password_hasher.mock import MockPasswordHasher
from health_backend.infra.doctor_profile.repository.in_memory import InMemoryDoctorProfileRepository
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
def admin_user() -> User:
    user = user_factory()
    user.add_role(UserRole.ADMIN)
    return user


@pytest.fixture
def input_data() -> SignUpDoctorProfileInput:
    return SignUpDoctorProfileInput(
        first_name='John',
        last_name='Doe',
        email='johndoe@examle.com',
        password='password',
    )


@pytest.fixture
def password_hasher() -> MockPasswordHasher:
    return MockPasswordHasher()


@pytest.mark.asyncio
async def test_valid(
    admin_user: User,
    input_data: SignUpDoctorProfileInput,
    password_hasher: MockPasswordHasher,
) -> None:
    user_repo = InMemoryUserRepository()
    doctor_profile_repo = InMemoryDoctorProfileRepository()
    sign_up_use_case = DoctorSignUp(
        user_repo=user_repo,
        doctor_profile_repo=doctor_profile_repo,
        password_hasher=password_hasher,
    )
    result = await sign_up_use_case.execute(input_data)

    doctor_user = await user_repo.get_by_id(result.user_id)
    assert doctor_user is not None
    assert doctor_user.is_doctor
    assert doctor_user.is_activation_pending

    approve_use_case = ApproveDoctorSignUp(
        user_repo=user_repo,
        identity_provider=MockIdentityProvider(admin_user),
    )
    await approve_use_case.execute(result.user_id)

    doctor_user = await user_repo.get_by_id(result.user_id)
    assert doctor_user is not None
    assert doctor_user.is_doctor
    assert doctor_user.is_active
