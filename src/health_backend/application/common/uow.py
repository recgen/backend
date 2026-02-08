from abc import abstractmethod
from typing import Protocol


class UnitOfWork(Protocol):
    @abstractmethod
    def add(self, instance: object) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...
