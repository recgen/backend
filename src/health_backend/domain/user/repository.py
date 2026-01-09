from abc import ABC, abstractmethod

from health_backend.domain.user.entity import User


class UserRepository(ABC):
    @abstractmethod
    async def add(self, user: User) -> None: ...
