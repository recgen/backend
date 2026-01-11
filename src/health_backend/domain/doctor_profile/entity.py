from dataclasses import dataclass
from typing import NewType, Self
from uuid import UUID, uuid4

from health_backend.domain.user.entity import UserId

DoctorProfileId = NewType('DoctorProfileId', UUID)


@dataclass
class DoctorProfile:
    id: DoctorProfileId
    user_id: UserId

    @classmethod
    def new(cls, user_id: UserId) -> Self:
        return cls(
            id=DoctorProfileId(uuid4()),
            user_id=user_id,
        )
