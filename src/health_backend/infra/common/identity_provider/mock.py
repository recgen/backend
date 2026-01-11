from dataclasses import dataclass
from uuid import UUID

from health_backend.application.common.identity_provider import IdentityProvider
from health_backend.domain.user.entity import User, UserId


@dataclass
class MockIdentityProvider(IdentityProvider):
    user: User | None

    async def get_current_user_id(self) -> UserId | None:
        if self.user:
            return self.user.id
        return None

    async def get_current_user(self) -> User | None:
        return self.user
