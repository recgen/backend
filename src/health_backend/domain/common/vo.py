from dataclasses import dataclass
from decimal import Decimal
from typing import Self


@dataclass(frozen=True, slots=True)
class Range:
    minimum: Decimal
    maximum: Decimal

    def contains(self, value: Decimal) -> bool:
        return self.minimum <= value <= self.maximum

    @classmethod
    def create[T: str | int | float | Decimal](cls, minimum: T, maximum: T) -> Self:
        return cls(minimum=Decimal(minimum), maximum=Decimal(maximum))
