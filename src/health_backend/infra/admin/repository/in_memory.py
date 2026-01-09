from uuid import UUID
from health_backend.domain.admin.entity import Admin
from health_backend.domain.admin.repository import AdminRepository


class InMemoryAdminRepository(AdminRepository):
    def __init__(self) -> None:
        self._data: list[Admin] = []

    async def get_by_user_id(self, user_id: UUID) -> Admin | None:
        selected = [admin for admin in self._data if admin.user_id == user_id]
        if not selected:
            return None
        return selected[0]

    async def add(self, admin: Admin) -> None:
        self._data.append(admin)
