from dataclasses import dataclass

from health_backend.application.common.errors import (
    ForbiddenActionError,
    UnauthorizedError,
    UserDoesNotExist,
    UserIsNotDoctor,
    WrongUserStatus,
)
from health_backend.application.common.identity_provider import IdentityProvider
from health_backend.domain.user.entity import UserId, UserStatus
from health_backend.domain.user.repository import UserRepository


@dataclass
class ApproveDoctorSignUp:
    user_repo: UserRepository
    identity_provider: IdentityProvider

    async def execute(self, doctor_user_id: UserId) -> None:
        current_user = await self.identity_provider.get_current_user()
        if current_user is None:
            raise UnauthorizedError
        if not current_user.can_approve_doctor_sign_up:
            raise ForbiddenActionError

        doctor_user = await self.user_repo.get_by_id(doctor_user_id)
        if doctor_user is None:
            raise UserDoesNotExist
        if not doctor_user.is_doctor:
            raise UserIsNotDoctor
        if not doctor_user.is_activation_pending:
            raise WrongUserStatus

        doctor_user.set_status(UserStatus.ACTIVE)
        await self.user_repo.update(doctor_user)
