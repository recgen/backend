from dataclasses import dataclass


@dataclass
class SignUpDoctorProfileInput:
    first_name: str
    last_name: str
    email: str
    password: str


@dataclass
class SignUpDoctorProfileOutput:
    first_name: str
    last_name: str
    email: str
