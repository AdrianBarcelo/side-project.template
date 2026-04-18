from abc import ABC
from dataclasses import dataclass
from typing import Any, Self


@dataclass(frozen=True)
class ValueObject(ABC):
    value: Any

    @classmethod
    def create_or_null(cls, value: Any | None) -> Self | None:
        if value is None:
            return None

        return cls(value)

    def __post_init__(self) -> None:
        self._assert_valid()

    def _assert_valid(self) -> None:
        pass
