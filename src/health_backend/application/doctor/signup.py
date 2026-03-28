from dataclasses import dataclass

from health_backend.application.common.access_token_generator import AccessTokenGenerator
from health_backend.application.common.committer import Committer
from health_backend.application.common.password_hasher import PasswordHasher
from health_backend.application.doctor.dto import (
    DoctorAuthResponse,
    DoctorDTO,
    DoctorSignupRequest,
)
from health_backend.domain.doctor.entity import Doctor
from health_backend.domain.doctor.repository import DoctorRepository


@dataclass(frozen=True, slots=True)
class DoctorSignup:
    repo: DoctorRepository
    committer: Committer
    password_hasher: PasswordHasher
    access_token_generator: AccessTokenGenerator

    async def execute(self, request: DoctorSignupRequest) -> DoctorAuthResponse:
        doctor = Doctor.create(
            name=request.name,
            email=request.email,
            hashed_password=self.password_hasher.hash(request.password),
        )

        await self.repo.add(doctor)

        token = self.access_token_generator.generate(
            doctor_id=doctor.id,
            expire_in=(60 * 60 * 24 * 30),  # thirty days
        )

        await self.committer.commit()
        return DoctorAuthResponse(
            access_token=token.value,
            doctor=DoctorDTO.from_entity(doctor),
        )
