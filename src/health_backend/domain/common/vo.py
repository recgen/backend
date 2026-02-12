import re
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Self

from health_backend.domain.common.errors import EmptyName, InvalidEmail


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


EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9!#$%&\'*+\-/=?^_`{|}~.]+'
    r'@'
    r'[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?'
    r'(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*'
    r'\.[a-zA-Z]{2,}$'
)


@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not EMAIL_REGEX.match(self.value):
            raise InvalidEmail


class Gender(StrEnum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
