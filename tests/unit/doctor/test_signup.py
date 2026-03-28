import pytest

from health_backend.application.doctor.dto import DoctorSignupRequest
from health_backend.application.doctor.signup import DoctorSignup
from health_backend.domain.common.errors import InvalidEmailError
from health_backend.domain.doctor.repository import DoctorRepository


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'email',
    [
        'qwerty',
        '',
        '@something',
        '@something.com',
        'some@thing',
        'something@@',
        'something@@hello.com',
        '1@2.a',
        '1@2.24',
    ],
)
async def test_signup_with_invalid_email_fails(signup_interactor: DoctorSignup, email: str) -> None:
    request = DoctorSignupRequest(name='John Doe', email=email, password='password')

    with pytest.raises(InvalidEmailError):
        await signup_interactor.execute(request)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'email',
    [
        'qwerty@hello.com',
        '1@2.co',
    ],
)
async def test_signup_with_valid_email_succeeds(
    signup_interactor: DoctorSignup, doctor_repository: DoctorRepository, email: str
) -> None:
    request = DoctorSignupRequest(name='John Doe', email=email, password='password')

    response = await signup_interactor.execute(request)

    doctor_by_id = await doctor_repository.get_by_id(response.doctor.id)
    assert doctor_by_id is not None
