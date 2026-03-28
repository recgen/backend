from dataclasses import dataclass
from uuid import UUID

import jwt

from health_backend.application.common.access_token_generator import AccessToken
from health_backend.application.common.errors import UnauthorizedError
from health_backend.application.common.idp import DoctorIdProvider
from health_backend.domain.doctor.entity import DoctorId

algorithm = 'HS256'


@dataclass(frozen=True, slots=True)
class JWTParser:
    secret: str

    def parse(self, token: str | None) -> AccessToken:
        if token is None:
            raise UnauthorizedError
        try:
            payload = jwt.decode(token, key=self.secret, algorithms=[algorithm])
        except jwt.PyJWTError as err:
            raise UnauthorizedError from err
        try:
            doctor_id = DoctorId(UUID(payload['sub']))
        except KeyError as err:
            raise UnauthorizedError from err
        return AccessToken(
            value=token,
            doctor_id=doctor_id,
        )


@dataclass(slots=True)
class JWTIdProvider(DoctorIdProvider):
    parser: JWTParser
    token: str | None
    _parsed_token: AccessToken | None = None

    def get_id(self) -> DoctorId | None:
        if self._parsed_token is None:
            self._parsed_token = self.parser.parse(self.token)
        return self._parsed_token.doctor_id
