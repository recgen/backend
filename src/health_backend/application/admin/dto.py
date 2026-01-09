from dataclasses import dataclass
from uuid import UUID


@dataclass
class CreateDoctorInput:
    first_name: str
    last_name: str
    email: str
    password_hash: str
    department_id: UUID


@dataclass
class CreateDoctorOutput:
    user_id: UUID
    first_name: str
    last_name: str
    email: str
    department_id: UUID
