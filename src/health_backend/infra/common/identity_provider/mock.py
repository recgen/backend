from dataclasses import dataclass
from uuid import UUID

from health_backend.application.common.identity_provider import IdentityProvider
from health_backend.domain.user.entity import User


@dataclass
class MockIdentityProvider(IdentityProvider):
    user: User

    async def get_current_user_id(self) -> UUID:
        return self.user.id
