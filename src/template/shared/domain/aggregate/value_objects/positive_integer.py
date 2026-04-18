from pydantic.dataclasses import dataclass

from template.shared.domain.aggregate.value_objects.exceptions.integer_is_not_positive import IntegerIsNotPositive
from template.shared.domain.aggregate.value_objects.value_object import ValueObject


@dataclass(frozen=True)
class PositiveInteger(ValueObject):
    value: int

    def _assert_valid(self) -> None:
        if not isinstance(self.value, int) or self.value <= 0:
            raise IntegerIsNotPositive(self.value)

    def __gt__(self, other: "PositiveInteger") -> bool:
        return self.value > other.value
