from typing import Any, Protocol


class UnitOfWork(Protocol):
    async def add(self, entity: Any) -> None: ...

    async def commit(self) -> None: ...
