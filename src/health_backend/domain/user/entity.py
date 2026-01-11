from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import NewType, Self
from uuid import UUID, uuid4

UserId = NewType('UserId', UUID)


class UserStatus(StrEnum):
    ACTIVATION_PENDING = 'ACTIVATION_PENDING'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'


class UserRole(StrEnum):
    ADMIN = 'ADMIN'
    DOCTOR = 'DOCTOR'


@dataclass
class User:
    id: UserId
    first_name: str
    last_name: str
    email: str
    password_hash: str
    status: UserStatus
    roles: list[UserRole]

    @classmethod
    def new(
        cls,
        first_name: str,
        last_name: str,
        email: str,
        password_hash: str,
        status: UserStatus,
        roles: list[UserRole],
    ) -> Self:
        return cls(
            id=UserId(uuid4()),
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash,
            status=status,
            roles=roles,
        )

    def set_status(self, status: UserStatus) -> None:
        self.status = status

    def add_role(self, role: UserRole) -> None:
        if not self.has_role(role):
            self.roles.append(role)

    def remove_role(self, role: UserRole) -> None:
        if self.has_role(role):
            self.roles.remove(role)

    @property
    def is_admin(self) -> bool:
        return self.has_role(UserRole.ADMIN)

    @property
    def is_doctor(self) -> bool:
        return self.has_role(UserRole.DOCTOR)

    @property
    def can_approve_doctor_sign_up(self) -> bool:
        return self.is_admin and self.is_active

    def has_role(self, role: UserRole) -> bool:
        return role in self.roles

    @property
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE

    @property
    def is_activation_pending(self) -> bool:
        return self.status == UserStatus.ACTIVATION_PENDING
