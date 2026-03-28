from dataclasses import dataclass

from health_backend.application.common.access_token_generator import AccessTokenGenerator
from health_backend.application.common.errors import NotFoundError, UnauthorizedError
from health_backend.application.common.password_hasher import PasswordHasher
from health_backend.application.doctor.dto import DoctorAuthResponse, DoctorDTO, DoctorLoginRequest
from health_backend.domain.common.vo import Email
from health_backend.domain.doctor.repository import DoctorRepository


@dataclass(frozen=True, slots=True)
class DoctorLogin:
    repo: DoctorRepository
    password_hasher: PasswordHasher
    access_token_generator: AccessTokenGenerator

    async def execute(self, request: DoctorLoginRequest) -> DoctorAuthResponse:
        doctor = await self.repo.get_by_email(Email(request.email))
        if doctor is None:
            raise NotFoundError
        if self.password_hasher.verify(request.password, doctor.hashed_password) is False:
            raise UnauthorizedError
        token = self.access_token_generator.generate(doctor.id, expire_in=(60 * 60 * 24 * 30))
        return DoctorAuthResponse(
            access_token=token.value,
            doctor=DoctorDTO.from_entity(doctor),
        )
