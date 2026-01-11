from health_backend.domain.user.entity import User, UserId
from health_backend.domain.user.repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._data: list[User] = []

    async def add(self, user: User) -> None:
        self._data.append(user)

    async def get_by_email(self, email: str) -> User | None:
        for user in self._data:
            if user.email == email:
                return user

    async def get_by_id(self, id: UserId) -> User | None:
        for user in self._data:
            if user.id == id:
                return user

    async def update(self, user: User) -> None:
        for old_user in self._data:
            if old_user.id == user.id:
                old_user, user = user, old_user
