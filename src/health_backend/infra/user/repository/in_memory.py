from health_backend.domain.user.entity import User
from health_backend.domain.user.repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._data: list[User] = []

    async def add(self, user: User) -> None:
        self._data.append(user)
