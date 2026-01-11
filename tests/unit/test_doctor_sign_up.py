import pytest

from health_backend.application.common.errors import EmailAlreadyInUse
from health_backend.application.doctor.dto import SignUpDoctorProfileInput
from health_backend.application.doctor.sign_up import DoctorSignUp
from health_backend.domain.user.entity import User, UserStatus
from health_backend.infra.common.password_hasher.mock import MockPasswordHasher, PasswordHasher
from health_backend.infra.doctor_profile.repository.in_memory import InMemoryDoctorProfileRepository
from health_backend.infra.user.repository.in_memory import InMemoryUserRepository


@pytest.fixture
def repos():
    return {
        'user': InMemoryUserRepository(),
        'doctor_profile': InMemoryDoctorProfileRepository(),
    }


@pytest.fixture
def use_case(repos) -> DoctorSignUp:
    return DoctorSignUp(
        user_repo=repos['user'],
        doctor_profile_repo=repos['doctor_profile'],
        password_hasher=MockPasswordHasher(),
    )


@pytest.fixture
def input_data() -> SignUpDoctorProfileInput:
    return SignUpDoctorProfileInput(
        first_name='John',
        last_name='Doe',
        email='johndoe@examle.com',
        password='johndoe69',
    )


@pytest.mark.asyncio
async def test_doctor_sign_up_valid(
    input_data: SignUpDoctorProfileInput, use_case: DoctorSignUp
) -> None:
    result = await use_case.execute(input_data)

    assert result.first_name == input_data.first_name
    assert result.last_name == input_data.last_name
    assert result.email == input_data.email

    user_repo = use_case.user_repo
    new_user = await user_repo.get_by_email(input_data.email)

    assert new_user is not None
    assert new_user.first_name == input_data.first_name
    assert new_user.last_name == input_data.last_name
    assert new_user.email == input_data.email
    assert new_user.status == UserStatus.ACTIVATION_PENDING
    assert new_user.is_doctor is True


@pytest.mark.asyncio
async def test_doctor_sign_up_email_already_used(
    input_data: SignUpDoctorProfileInput, use_case: DoctorSignUp
) -> None:
    user_with_same_email = User.new(
        first_name='OriginalJohn',
        last_name='Doe',
        email='johndoe@examle.com',
        password_hash='xxxyyyzzz',
        status=UserStatus.ACTIVE,
        roles=[],
    )
    await use_case.user_repo.add(user_with_same_email)
    with pytest.raises(EmailAlreadyInUse):
        await use_case.execute(input_data)
