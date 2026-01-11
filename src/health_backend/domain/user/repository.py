from abc import ABC, abstractmethod

from health_backend.domain.user.entity import User, UserId


class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_by_id(self, id: UserId) -> User | None: ...
