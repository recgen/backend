from abc import ABC, abstractmethod

from health_backend.domain.user.entity import User, UserId


class IdentityProvider(ABC):
    @abstractmethod
    async def get_current_user_id(self) -> UserId | None: ...

    @abstractmethod
    async def get_current_user(self) -> User | None: ...
