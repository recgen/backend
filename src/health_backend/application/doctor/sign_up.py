from dataclasses import dataclass

from health_backend.application.common.errors import EmailAlreadyInUse
from health_backend.application.common.identity_provider import IdentityProvider
from health_backend.application.common.password_hasher import PasswordHasher
from health_backend.application.doctor.dto import (
    SignUpDoctorProfileInput,
    SignUpDoctorProfileOutput,
)
from health_backend.domain.doctor_profile.entity import DoctorProfile
from health_backend.domain.doctor_profile.repository import DoctorProfileRepository
from health_backend.domain.user.entity import User, UserRole, UserStatus
from health_backend.domain.user.repository import UserRepository


@dataclass
class DoctorSignUp:
    user_repo: UserRepository
    doctor_profile_repo: DoctorProfileRepository
    password_hasher: PasswordHasher

    async def execute(self, input_data: SignUpDoctorProfileInput) -> SignUpDoctorProfileOutput:
        user_by_email = await self.user_repo.get_by_email(input_data.email)
        if user_by_email is not None:
            raise EmailAlreadyInUse

        password_hash = self.password_hasher.hash(input_data.password)

        user = User.new(
            first_name=input_data.first_name,
            last_name=input_data.last_name,
            email=input_data.email,
            password_hash=password_hash,
            status=UserStatus.ACTIVATION_PENDING,
            roles=[UserRole.DOCTOR],
        )
        doctor_profile = DoctorProfile.new(user_id=user.id)

        await self.user_repo.add(user)
        await self.doctor_profile_repo.add(doctor_profile)

        return SignUpDoctorProfileOutput(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
