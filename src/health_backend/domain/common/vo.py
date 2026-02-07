from dataclasses import dataclass
from decimal import Decimal
from typing import Self

from health_backend.domain.common.errors import EmptyEmail, EmptyName


@dataclass(frozen=True, slots=True)
class Range:
    minimum: Decimal
    maximum: Decimal

    def contains(self, value: Decimal) -> bool:
        return self.minimum <= value <= self.maximum

    @classmethod
    def create[T: str | int | float | Decimal](cls, minimum: T, maximum: T) -> Self:
        return cls(minimum=Decimal(minimum), maximum=Decimal(maximum))


@dataclass(frozen=True, slots=True)
class Name:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) == 0:
            raise EmptyName


@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) == 0:
            raise EmptyEmail
        # TODO: validation
