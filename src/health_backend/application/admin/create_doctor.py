from dataclasses import dataclass
from uuid import uuid4

from health_backend.application.admin.dto import CreateDoctorInput, CreateDoctorOutput
from health_backend.application.common.exceptions import UnauthorizedError
from health_backend.application.common.identity_provider import IdentityProvider
from health_backend.domain.admin.repository import AdminRepository
from health_backend.domain.doctor.entity import Doctor
from health_backend.domain.doctor.repository import DoctorRepository
from health_backend.domain.user.entity import User
from health_backend.domain.user.repository import UserRepository


@dataclass
class CreateDoctor:
    identity_provider: IdentityProvider
    admin_repo: AdminRepository
    doctor_repo: DoctorRepository
    user_repo: UserRepository

    async def execute(self, input_data: CreateDoctorInput) -> CreateDoctorOutput:
        user_id = await self.identity_provider.get_current_user_id()
        admin = await self.admin_repo.get_by_user_id(user_id)
        if admin is None:
            raise UnauthorizedError
        user = User(
            id=uuid4(),
            first_name=input_data.first_name,
            last_name=input_data.last_name,
            email=input_data.email,
            password_hash=input_data.password_hash,
        )
        await self.user_repo.add(user)
        doctor = Doctor(
            user_id=user.id,
            department_id=input_data.department_id,
        )
        await self.doctor_repo.add(doctor)
        return CreateDoctorOutput(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            department_id=doctor.department_id,
        )
