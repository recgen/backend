import time
from dataclasses import dataclass

import jwt

from health_backend.application.common.access_token_generator import (
    AccessToken,
    AccessTokenGenerator,
)
from health_backend.domain.doctor.entity import DoctorId

algorithm = 'HS256'


@dataclass(frozen=True, slots=True)
class JWTGenerator(AccessTokenGenerator):
    secret: str

    def generate(self, doctor_id: DoctorId, expire_in: int) -> AccessToken:
        now = int(time.time())
        token = jwt.encode(
            payload={
                'sub': str(doctor_id),
                'exp': now + expire_in,
                'iat': now,
            },
            key=self.secret,
        )
        return AccessToken(token, doctor_id=doctor_id)
