from abc import ABC, abstractmethod
from uuid import UUID

from health_backend.domain.admin.entity import Admin


class AdminRepository(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Admin | None: ...

    @abstractmethod
    async def add(self, admin: Admin) -> None: ...
