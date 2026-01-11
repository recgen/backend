from dataclasses import dataclass

from health_backend.domain.user.entity import UserId


@dataclass
class SignUpDoctorProfileInput:
    first_name: str
    last_name: str
    email: str
    password: str


@dataclass
class SignUpDoctorProfileOutput:
    user_id: UserId
    first_name: str
    last_name: str
    email: str
