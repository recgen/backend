from health_backend.application.common.access_token_generator import (
    AccessToken,
    AccessTokenGenerator,
)
from health_backend.application.common.password_hasher import PasswordHasher
from health_backend.domain.doctor.entity import DoctorId


class FakePasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return password

    def verify(self, password: str, hashed_password: str) -> bool:
        return password == hashed_password


class FakeAccessTokenGenerator(AccessTokenGenerator):
    def generate(self, doctor_id: DoctorId, expire_in: int) -> AccessToken:  # noqa: ARG002
        return AccessToken(value=str(doctor_id), doctor_id=doctor_id)
